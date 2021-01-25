import json
from flask import request, jsonify, flash, render_template
from flask_login import current_user
from sqlalchemy import or_, desc, func

from forms.book import SearchForm
from gather.ye_book import YeBook
from libs.helper import is_isbn_or_key
from models.base import db
from models.book import Book
from models.gift import Gift
from models.user import User
from models.wish import Wish
from view_models.book import BookCollection, BookViewModel
from view_models.trade import TradeInfo
from .blueprint import web


@web.route('/book/search')
def search():
	form = SearchForm(request.args)
	books = BookCollection()

	if form.validate():
		q = form.q.data.strip()
		page = form.page.data
		isbn_or_key = is_isbn_or_key(q)
		ye_book = YeBook()

		if isbn_or_key == 'isbn':
			ye_book.search_by_isbn(q)
		else:
			ye_book.search_by_keyword(q, page)

		books.fill(ye_book, q)
		# return json.dumps(books, default=lambda o: o.__dict__), 200, {'content-type': 'application/json'}
	else:
		print(form.errors)
		flash('搜索的关键字不符合要求，请重新输入关键字')
	return render_template('search_result.html', books=books, form=form)
	# return jsonify({'message': form.errors})


@web.route('/search')
def search_book():
	# from web.right_menus import popular_gifters_list, popular_wishes_list
	q = request.args.get('q').strip()
	page = int(request.args.get('page', 1))
	per_page = 10
	page_data = None
	if q and page:
		isbn_or_key = is_isbn_or_key(q)
		if isbn_or_key == 'isbn':
			page_data = Book.query.filter_by(isbn=q).paginate(page=page, per_page=per_page)
		else:
			page_data = Book.query.filter(
				or_(Book.title.like('%{}%'.format(q)),
					Book.author.like('%{}%'.format(q)))
			).order_by(desc(Book.pub_date)).paginate(page=page, per_page=per_page)

	html = render_template('search_result.html',
						   page_data=page_data,
						   q=q)
	return html


@web.route('/search/more/<q>')
def search_more(q):
	page = int(request.args.get('page', 1))
	per_page = 10
	try:
		page_data = Book.query.filter(
			or_(Book.title.like('%{}%'.format(q)),
				Book.author.like('%{}%'.format(q)))
		).order_by(desc(Book.pub_date)).paginate(page=page, per_page=per_page)
		html = render_template('search_more.html', page_data=page_data)
		return jsonify({'code': 0, 'data': html})
	except Exception as e:
		# print(e)
		data = ''
	return jsonify({'code': 1, 'data': data})


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
	""" 书籍详情页 """
	# from web.right_menus import popular_gifters_list, popular_wishes_list
	has_in_gifts = False
	has_in_wishes = False
	# book detail
	ye_book = YeBook()
	ye_book.search_by_isbn(isbn)
	book = BookViewModel(ye_book.first)

	if current_user.is_authenticated:
		gift_user = Gift.query.filter_by(user=current_user, isbn=isbn, launched=False, status=1).first()
		wish_user = Wish.query.filter_by(user=current_user, isbn=isbn, launched=False, status=1).first()

		if gift_user:
			has_in_gifts = True

		if wish_user:
			has_in_wishes = True


	# all gifters
	trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False, status=1).all()
	# all wishers
	trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False, status=1).all()
	#
	trade_gifts_model = TradeInfo(trade_gifts)
	trade_wishes_model = TradeInfo(trade_wishes)

	return render_template('book_detail.html',
						   book=book,
						   wishes=trade_wishes_model,
						   gifts=trade_gifts_model,
						   has_in_gifts=has_in_gifts,
						   has_in_wishes=has_in_wishes)





