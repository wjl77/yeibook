import hashlib
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from gather.ye_book import YeBook
from libs.enums import PendingStatus
from libs.helper import is_isbn_or_key
from models.base import db, Base
from models.drift import Drift
from models.gift import Gift
from models.wish import Wish


class User(UserMixin, Base):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), nullable=False, unique=True)
	_password = db.Column('password', db.String(256), nullable=False)
	nickname = db.Column(db.String(24), nullable=False, unique=True)
	phone_number = db.Column(db.String(18), unique=True)
	confirmed = db.Column(db.Boolean, default=False)
	leaves = db.Column(db.Float, default=0)
	send_counter = db.Column(db.Integer, default=0)
	receive_counter = db.Column(db.Integer, default=0)
	wx_open_id = db.Column(db.String(50))
	wx_name = db.Column(db.String(32))
	wx_avatar = db.Column(db.String(128), default='1.gif')
	is_admin = db.Column(db.Integer, default=0)

	@property
	def user_head(self):
		return '/static/avatars/' + self.wx_avatar

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, raw):
		# raw => 原始明文密码
		self._password = hashlib.sha256(raw.encode()).hexdigest()

	def check_password(self, raw):
		raw = hashlib.sha256(raw.encode()).hexdigest()
		if raw == self._password:
			return True
		return False

	def can_save_to_list(self, isbn):
		if is_isbn_or_key(isbn) != 'isbn':
			return False
		ye_book = YeBook()
		ye_book.search_by_isbn(isbn)
		if not ye_book.first:
			return False
		# 不允许用户同时赠送多本相同的图书
		# 不能同时成为赠送者和索要者
		gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False, status=1).first()
		wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False, status=1).first()
		if gifting or wishing:
			return False
		return True

	def generate_token(self, expiration=600):
		s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
		return s.dumps({'id': self.id}).decode('utf-8')

	@staticmethod
	def reset_password(token, new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		uid = data.get('id')
		with db.auto_commit():
			user = User.query.get(uid)
			if not user:
				return False
			user.password = new_password
		return True

	def can_send_drift(self):
		if self.leaves < 1:
			return False
		# 已赠送书籍
		success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
		# 已接收书籍
		success_receive_count = Drift.query.filter_by(
			requester_id=self.id,
			pending=PendingStatus.Success).count()

		if (success_receive_count // 2) <= success_gifts_count:
			return True
		return False

	@property
	def summary(self):
		return dict(
			nickname=self.nickname,
			beans=self.leaves,
			email=self.email,
			send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
		)



	# def get_id(self):
	# 	return self.id











