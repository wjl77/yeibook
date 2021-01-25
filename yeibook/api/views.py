from flask import Blueprint, jsonify, request
from sqlalchemy import or_, desc
from models.book import Book

api = Blueprint('api', __name__)


@api.route('/v2/book/isbn/<isbn>')
def by_isbn(isbn):
	book = Book.query.filter_by(isbn=isbn).first_or_404()
	if book:
		book_data = {
			'author': book.author,
			'category': book.category,
			'rating': book.rating,
			'price': book.price,
			'image': book.img_url,
			'isbn': book.isbn,
			'pubdate': book.pub_date,
			# 'publisher': book.info.split('/')[-2].strip(),
			'title': book.title,
			'intro': book.intro,
			'info': book.info.split('/')[1].strip() + ' | ' + book.info.split('/')[2].strip()
		}
		return jsonify(book_data), 200


@api.route('/v2/book/search')
def by_keyword():
	q = request.args.get('q')
	count = int(request.args.get('count', 15))
	start = int(request.args.get('start', 0))
	if q:
		books = Book.query.filter(
			or_(Book.title.like('%{}%'.format(q)),
				Book.author.like('%{}%'.format(q)))
		).order_by(desc(Book.pub_date)).all()
		books_list = []
		if books:
			for book in books:
				book_data = {
					'author': book.author,
					'category': book.category,
					'price': book.price,
					'rating': book.rating,
					'image': book.img_url,
					'isbn': book.isbn,
					'pubdate': book.pub_date,
					'title': book.title,
					'intro': book.intro,
					'info': book.info
				}
				books_list.append(book_data)
			total = len(books_list)
			books_list = books_list[start:start+count]
			books_data = {
				'books': books_list,
				'total': total
			}
			result = books_data
		else:
			books_data = {}
			result = books_data
		return jsonify(result), 200
