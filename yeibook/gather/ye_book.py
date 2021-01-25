from flask import jsonify
from sqlalchemy import or_, desc

from libs.httper import HTTP
from models.book import Book


class YeBook:

	# isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
	# keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start{}'
	def __init__(self):
		self.books = []
		self.total = 0

	def search_by_isbn(self, isbn):
		book = Book.query.filter_by(isbn=isbn).first()
		if book:
			isbn_data = {
				'author': book.author,
				'category': book.category,
				'rating': book.rating,
				'price': book.price,
				# 'image': '/static/cover/images/' + book.img,
				'image': book.img_url,
				'isbn': book.isbn,
				# 'pubdate': book.info.split('/')[-1].strip(),
				'pubdate': book.pub_date,
				'publisher': book.info.split('/')[-2].strip(),
				'title': book.title,
				'intro': book.intro,
				'info': book.info.split('/')[1].strip() + ' | ' + book.info.split('/')[2].strip(),
				# 'info': book.info
			}
			result = isbn_data
		else:
			isbn_data = {}
			result = isbn_data
		self.__fill_single(result)
		# url = cls.isbn_url.format(isbn)
		# result = HTTP.get(url)
		# return result

	def __fill_single(self, data):
		if data:
			self.total = 1
			self.books.append(data)

	def __fill_collection(self, data):
		if data:
			self.total = data['total']
			self.books = data['books']

	def search_by_keyword(self, keyword, page=1):
		# books = Book.query.filter(Book.title.like('%{}%'.format(keyword))).all() or \
		# 		Book.query.filter(Book.author.like('%{}%'.format(keyword))).all()

		books = Book.query.filter(
			or_(Book.title.like('%{}%'.format(keyword)),
				Book.author.like('%{}%'.format(keyword)))
		).order_by(desc(Book.pub_date)).all()

		books_list = []
		if books:
			for book in books:
				book_data = {
					'author': book.author,
					'category': book.category,
					'price': book.price,
					'rating': book.rating,
					# 'image': '/static/cover/images/' + book.img,
					'image': book.img_url,
					'isbn': book.isbn,
					# 'pubdate': book.info.split('/')[-1].strip(),
					'pubdate': book.pub_date,
					# 'publisher': book.info.split('/')[-2].strip(),
					'title': book.title,
					'intro': book.intro,
					'info': book.info
				}
				books_list.append(book_data)

			total = len(books_list)
			# 分页
			start = (page - 1) * 15
			counter = 15
			books_list = books_list[start:start+counter]
			books_data = {
				'books': books_list,
				'total': total
			}
			result = books_data
		else:
			books_data = {}
			result = books_data
		self.__fill_collection(result)

	@property
	def first(self):
		return self.books[0] if self.total >= 1 else None

		# start = (page - 1) * 15
		# count = 15

		# url = cls.keyword_url.format(keyword, count, start)
		# result = HTTP.get(url)
		# return result
