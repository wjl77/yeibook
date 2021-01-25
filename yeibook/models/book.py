from models.base import db, Base


class Book(Base):
	__tablename__ = 'book'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64), nullable=False)
	author = db.Column(db.String(300), default='未名')
	info = db.Column(db.String(256))
	intro = db.Column(db.String(2048))
	isbn = db.Column(db.String(15), nullable=False, unique=True)
	img = db.Column(db.String(64))
	img_url = db.Column(db.String(1024))
	rating = db.Column(db.String(10))
	price = db.Column(db.String(20))
	category = db.Column(db.String(32))
	pub_date = db.Column(db.String(32))

