from sqlalchemy import desc, func
from gather.ye_book import YeBook
from models.base import db, Base


class Gift(Base):
	__tablename__ = 'gift'
	id = db.Column(db.Integer, primary_key=True)
	launched = db.Column(db.Boolean, default=False)
	message = db.Column(db.String(1024))
	user = db.relationship('User', backref=db.backref('user_list', lazy='dynamic'))
	uid = db.Column(db.Integer, db.ForeignKey('user.id'))
	book = db.relationship('Book', backref=db.backref('gift_list', lazy='dynamic'))
	bid = db.Column(db.Integer, db.ForeignKey('book.id'))
	isbn = db.Column(db.String(15), nullable=False)

	def is_yourself_gift(self, uid):
		return True if uid == self.uid else False

	@property
	def announced_time(self):
		# return self.create_time.strftime('%Y-%m-%d')
		return self.create_time

	@classmethod
	def get_user_gifts(cls, uid):
		gifts = Gift.query.filter_by(uid=uid, launched=False, status=1).order_by(
			desc(Gift.create_time)).all()
		return gifts

	@classmethod
	def get_wish_counts(cls, isbn_list):
		from models.wish import Wish
		count_list = db.session.query(Wish.isbn, func.count(Wish.id)).filter(Wish.launched == False,
									  Wish.status == 1,
									  Wish.isbn.in_(isbn_list)
									  ).group_by(Wish.isbn).all()
		count_list = [{'isbn': w[0], 'count': w[1]} for w in count_list]
		return count_list

	@property
	def gift_book(self):
		ye_book = YeBook()
		ye_book.search_by_isbn(self.isbn)
		return ye_book.first

	@classmethod
	def recent(cls):
		""" 最近的礼物 """
		per_page = 2
		page = 1
		# recent_gift = Gift.query.filter_by(launched=False, status=1).group_by(
		# 	Gift.isbn).order_by(desc(Gift.create_time)).limit(30).all()

		page_data = Gift.query.filter_by(launched=False, status=1).group_by(
			Gift.isbn).order_by(desc(Gift.create_time)).paginate(page=page, per_page=per_page)
		return page_data

