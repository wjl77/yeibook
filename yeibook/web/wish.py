from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from libs.email import send_mail
from models.base import db
from models.gift import Gift
from models.wish import Wish
from view_models.wish import MyWishes
from .blueprint import web

__author__ = '子良'


@web.route('/my/wish')
@login_required
def my_wish():
    """ 心愿清单 """
    # from web.right_menus import popular_gifters_list, popular_wishes_list
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid=uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_counts(isbn_list=isbn_list)
    view_model = MyWishes(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html',
                           wishes=view_model.wishes)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    """ 加入到心愿清单 """
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.user = current_user
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash('这本书已在你的赠送清单或心愿清单，不能重复添加', category='warning')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    """ 向他人赠送我的礼物 """
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(isbn=wish.isbn, uid=current_user.id, status=1).first()
    if not gift:
        flash('你还没有上传此书，请点击"加入到赠送清单"，请确保自己可以赠送此书', category='warning')
    else:
        send_mail(wish.user.email,
                  '有人想送你一本书',
                  'email/satisify_wish.html',
                  wish=wish,
                  gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将会收到一个飘叶', category='success')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    """ 撤销心愿 """
    with db.auto_commit():
        wish = Wish.query.filter_by(isbn=isbn, launched=False, uid=current_user.id, status=1).first_or_404()
        wish.status = 0
    return redirect(url_for('web.my_wish'))
