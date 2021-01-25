from libs.enums import PendingStatus
from models.base import Base, db


class Drift(Base):
	id = db.Column(db.Integer, primary_key=True)
	# 收件信息
	recipient_name = db.Column(db.String(20), nullable=False)
	address = db.Column(db.String(100), nullable=False)
	mobile = db.Column(db.String(20), nullable=False)
	# 给赠书人的留言
	message = db.Column(db.String(200))
	# 书籍信息
	isbn = db.Column(db.String(13))
	book_title = db.Column(db.String(50))
	book_author = db.Column(db.String(30))
	book_img = db.Column(db.String(50))
	# 请求者信息
	wx_id = db.Column(db.String(20))
	requester_id = db.Column(db.Integer)
	requester_nickname = db.Column(db.String(20))
	# 赠送者信息
	gifter_id = db.Column(db.Integer)
	gift_id = db.Column(db.Integer)
	gifter_nickname = db.Column(db.String(20))
	# 交易状态
	_pending = db.Column('pending', db.SmallInteger, default=1)

	# getter
	@property
	def pending(self):
		return PendingStatus(self._pending)

	@pending.setter
	def pending(self, status):
		self._pending = status.value


