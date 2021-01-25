from flask import render_template, request, jsonify
from sqlalchemy import desc

from gather.ye_book import YeBook
from models.gift import Gift
from view_models.book import BookViewModel
from .blueprint import web


__author__ = '七月'


@web.route('/')
def index():
    per_page = 2
    page = int(request.args.get('page', 1))
    page_data = Gift.query.filter_by(launched=False, status=1).group_by(
        Gift.isbn).order_by(desc(Gift.create_time)).paginate(page=page, per_page=per_page)
    # # page_data = Gift.recent()
    # # page_data = recent_gifts.pagination(page=page, per_page=per_page)
    # # html = render_template('index.html', recent=page_data)
    # recent_books = [BookViewModel(gift.gift_book, gift.publish_time) for gift in page_data.items]
    # # return render_template('index.html', recent=books)
    return render_template('index.html', page_data=page_data)


@web.route('/recent')
def recent():
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


@web.route('/personal')
def personal_center():
    pass
