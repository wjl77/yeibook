from models.base import Base, db


class LoginHistory(Base):
	__tablename__ = 'login_history'
	id = db.Column(db.Integer, primary_key=True)
	uip = db.Column(db.String(32))
	uag = db.Column(db.String(256))
	user = db.relationship('User')
	uid = db.Column(db.Integer, db.ForeignKey('user.id'))

