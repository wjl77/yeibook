from flask import flash, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from sqlalchemy import desc, or_

from forms.book import DriftForm
from libs.email import send_mail
from libs.enums import PendingStatus
from models.base import db
from models.drift import Drift
from models.gift import Gift
from models.user import User
from models.wish import Wish
from view_models.book import BookViewModel
from view_models.drift import DriftCollection
from .blueprint import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    """ 向他人请求此书 """
    current_gift = Gift.query.get(gid)
    uid = current_user.id
    form = DriftForm()

    if current_gift:

        if current_gift.is_yourself_gift(uid):
            flash('这本书是你自己的，自己不能向自己索要喔！', category='warning')
            return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

        wish = Wish.query.filter_by(uid=uid, isbn=current_gift.isbn, status=1, launched=False).first()
        if not wish:
            flash('您尚未将此书加入到心愿清单，请先加入到心愿清单', category='warning')
            return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

        can = current_user.can_send_drift()
        if not can:
            return render_template('not_enough_leaves.html', leaves=current_user.leaves)

        if form.validate_on_submit():
            save_drift(form, current_gift)
            send_mail(current_gift.user.email,
                      '有人想要您的书',
                      'email/get_gift.html',
                      wisher=current_user,
                      gift=current_gift)
            return redirect(url_for('web.pending'))
        else:
            if form.errors:
                flash('提交失败，请重试', category='warning')

        gifter = current_gift.user.summary
        return render_template('drift.html',
                               gid=gid,
                               gifter=gifter,
                               user_beans=current_user.leaves,
                               form=form)
    else:
        abort(404)


@web.route('/pending')
@login_required
def pending():
    """ 飘叶 """
    # from web.right_menus import popular_gifters_list, popular_wishes_list
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)
    ).order_by(desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html',
                           drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    """ 赠书者，拒绝 """
    with db.auto_commit():
        drift = Drift.query.filter(Drift.id == did, Gift.uid == current_user.id).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.leaves += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    """ 请求者，撤销 """
    with db.auto_commit():
        drift = Drift.query.filter_by(id=did, requester_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.leaves += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    """ 已邮寄 """
    with db.auto_commit():
        drift = Drift.query.filter(Drift.id == did, Gift.uid == current_user.id).first()
        drift.pending = PendingStatus.Success
        current_user.leaves += 1
        current_user.send_counter += 1
        gift = Gift.query.filter_by(id=drift.gift_id, launched=False, status=1).first()
        gift.launched = True

        wish = Wish.query.filter_by(uid=drift.requester_id,
                                    isbn=drift.isbn,
                                    launched=False,
                                    status=1).first()
        # print(wish)
        wish.launched = True
        wish.user.receive_counter += 1
        return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        drift.isbn = current_gift.isbn
        drift.book_title = BookViewModel(current_gift.gift_book).title
        drift.book_author = BookViewModel(current_gift.gift_book).author
        drift.book_img = BookViewModel(current_gift.gift_book).image

        current_user.leaves -= 1
        db.session.add(drift)
