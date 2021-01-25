from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from libs.enums import PendingStatus
from models.base import db
from models.drift import Drift
from models.gift import Gift
from view_models.gift import MyGifts
from .blueprint import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    """ 赠送清单 """
    # 显示当前用户的礼物清单
    # from web.right_menus import popular_gifters_list, popular_wishes_list
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid=uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list=isbn_list)
    view_model = MyGifts(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html',
                           gifts=view_model.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    """ 赠送此书 """
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.user = current_user
            current_user.leaves += current_app.config['LEAVES_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('这本书已在你的赠送清单或心愿清单，不能重复添加', category='warning')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    """ 撤销礼物 """
    # gift = Gift.query.filter_by(id=gid, uid=current_user.id, launched=False, status=1).first_or_404()
    gift = Gift.query.filter_by(id=gid, uid=current_user.id, launched=False, status=1).first()
    # drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Wating).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Wating).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往飘叶处理该交易')
    else:
        with db.auto_commit():
            current_user.leaves -= current_app.config['LEAVES_UPLOAD_ONE_BOOK']
            gift.status = 0
    return redirect(url_for('web.my_gifts'))



