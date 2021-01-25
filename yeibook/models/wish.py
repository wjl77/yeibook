from sqlalchemy import desc, func

from gather.ye_book import YeBook
from models.base import db, Base


class Wish(Base):
	__tablename__ = 'wish'
	id = db.Column(db.Integer, primary_key=True)
	launched = db.Column(db.Boolean, default=False)
	message = db.Column(db.String(256))
	user = db.relationship('User')
	uid = db.Column(db.Integer, db.ForeignKey('user.id'))
	book = db.relationship('Book')
	bid = db.Column(db.Integer, db.ForeignKey('book.id'))
	isbn = db.Column(db.String(15), nullable=False)

	@classmethod
	def get_user_wishes(cls, uid):
		wishes = Wish.query.filter_by(uid=uid, launched=False, status=1).order_by(
			desc(Wish.create_time)).all()
		return wishes

	@classmethod
	def get_gift_counts(cls, isbn_list):
		from models.gift import Gift
		count_list = db.session.query(Gift.isbn, func.count(Gift.id)).filter(Gift.launched == False,
																			 Gift.status == 1,
																			 Gift.isbn.in_(isbn_list)
																			 ).group_by(Gift.isbn).all()
		count_list = [{'isbn': w[0], 'count': w[1]} for w in count_list]
		return count_list

	@property
	def wish_book(self):
		ye_book = YeBook()
		ye_book.search_by_isbn(self.isbn)
		return ye_book.first
