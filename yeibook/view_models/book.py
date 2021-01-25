
def fill_price(price):
	if price[-1] == '币':
		price = price
	elif price[-1] != '元':
		price = price + '元'
	return price


class BookViewModel:
	def __init__(self, book, announced_time=None):
		self.title = book['title']
		# self.publisher = book['publisher']
		self.author = book['author']
		self.image = book['image']
		self.intro = book['intro']
		self.info = book['info']
		self.isbn = book['isbn']
		self.pubdate = book['pubdate']
		self.rating = book['rating']
		self.price = fill_price(book['price'])
		self.announced_time = announced_time


class BookCollection:
	def __init__(self):
		self.total = 0
		self.books = []
		self.keyword = ''

	def fill(self, ye_book, keyword):
		self.total = ye_book.total
		self.keyword = keyword
		self.books = [BookViewModel(book) for book in ye_book.books]

# class BookViewModel:
# 	@classmethod
# 	def package_single(cls, data, keyword):
# 		returned = {
# 			'books': [],
# 			'total': 0,
# 			'keyword': keyword
# 		}
# 		if data:
# 			returned['total'] = 1
# 			returned['books'] = [cls._cut_book_data(data)]
# 		return returned
#
# 	@classmethod
# 	def package_collection(cls, data, keyword):
# 		returned = {
# 			'books': [],
# 			'total': 0,
# 			'keyword': keyword
# 		}
# 		if data:
# 			returned['books'] = [cls._cut_book_data(book) for book in data['books']]
# 			returned['total'] = data['total']
# 		return returned
#
# 	@classmethod
# 	def _cut_book_data(cls, data):
# 		book = {
# 			'title': data['title'],
# 			'publisher': data['publisher'],
# 			'intro': data['intro'],
# 			'image': data['image'],
# 			'author': data['author']
# 		}
# 		return book

