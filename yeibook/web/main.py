import os

from flask import render_template, request, jsonify, flash
from flask_login import current_user, login_required
from sqlalchemy import desc, func
from werkzeug.utils import secure_filename

from forms.upload_avatar import AvatarForm
from gather.ye_book import YeBook
from models.base import db
from models.gift import Gift
from models.user import User
from models.wish import Wish
from view_models.book import BookViewModel
from .blueprint import web


__author__ = '七月'


@web.route('/current/gifts')
def current_gifts():
    """ 即时赠送信息 """
    gifts = Gift.query.filter_by(status=1, launched=0).all()
    if gifts:
        books = [{'nickname': gift.user.nickname, 'book_name': gift.gift_book['title']}
                 for gift in gifts]
        return jsonify({'code': 1, 'data': books})
    else:
        return jsonify({'code': 0, 'data': []})


@web.route('/')
def index():
    """ 首页 """
    per_page = 2
    page = int(request.args.get('page', 1))
    page_data = Gift.query.filter_by(launched=False, status=1).group_by(
        Gift.isbn).order_by(desc(Gift.create_time)).paginate(page=page, per_page=per_page)
    # # page_data = Gift.recent()
    # # page_data = recent_gifts.pagination(page=page, per_page=per_page)
    # # html = render_template('index.html', recent=page_data)
    # recent_books = [BookViewModel(gift.gift_book, gift.publish_time) for gift in page_data.items]
    # # return render_template('index.html', recent=books)
    return render_template('index.html',
                           page_data=page_data)


@web.route('/recent')
def recent():
    """ 最近赠书分页 """
    per_page = 2
    page = int(request.args.get('page', 1))

    try:
        page_data = Gift.query.filter_by(launched=False, status=1).group_by(
            Gift.isbn).order_by(desc(Gift.create_time)).paginate(page=page, per_page=per_page)
        recent_books = [BookViewModel(gift.gift_book, gift.announced_time) for gift in page_data.items]
        html = render_template('recent_gifts.html', recent=recent_books)
        return jsonify({'code': 0, 'data': html})
    except Exception as e:
        # print(e)
        data = ''

    return jsonify({'code': 1, 'data': data})


@web.route('/mine', methods=['GET', 'POST'])
@login_required
def mine():
    """ 个人中心 """
    # from web.right_menus import popular_gifters_list, popular_wishes_list
    img_path = r'D:\fishbook\static\avatars'
    form = AvatarForm()

    if form.validate_on_submit():
        avatar = form.avatar.data
        avatar_name = secure_filename(avatar.filename)
        avatar_path = os.path.join(img_path, avatar_name)
        avatar.save(avatar_path)
        with db.auto_commit():
            user = User.query.filter_by(id=current_user.id).first()
            user.wx_avatar = avatar_name
        flash('上传成功', category='success')
    else:
        if form.errors:
            flash('上传失败，只支持jpeg/jpg/png/gif格式的图片', category='warning')

    return render_template('mine.html',
                           form=form)


@web.route('/right/menus')
def right_menus():
    # 最受欢迎赠书者
    popular_gifters_list = []
    popular_gifters = db.session.query(
        Gift.uid, func.count(Gift.id)).filter(Gift.launched == True).group_by(
        Gift.uid).order_by(desc(func.count(Gift.id))).limit(10).all()

    for popular_gifter in popular_gifters:
        tmp_data = {}
        user = User.query.get(popular_gifter[0])
        count = popular_gifter[1]
        tmp_data['nickname'] = user.nickname
        tmp_data['count'] = count
        tmp_data['avatar'] = user.user_head
        popular_gifters_list.append(tmp_data)
    # print(popular_gifters_list)
    # 最受欢迎心愿
    popular_wishes_list = []
    popular_wishes = db.session.query(Wish.isbn, func.count(Wish.id)).filter(
        Wish.status == 1, Wish.launched == False).group_by(
        Wish.isbn).order_by(desc(func.count(Wish.id))).limit(10).all()
    # print(popular_wishes)

    for popular_wish in popular_wishes:
        ye_book = YeBook()
        tmp_data = {}
        ye_book.search_by_isbn(popular_wish[0])
        wish_title = ye_book.first['title']
        wish_image = ye_book.first['image']
        count = popular_wish[1]
        tmp_data['count'] = count
        tmp_data['wish_title'] = wish_title
        tmp_data['wish_image'] = wish_image
        popular_wishes_list.append(tmp_data)

    html = render_template('right_menus.html',
                           popular_gifters_list=popular_gifters_list,
                           popular_wishes_list=popular_wishes_list)

    return jsonify({'data': html})
