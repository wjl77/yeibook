from contextlib import contextmanager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery


class SQLAlchemy(_SQLAlchemy):
	@contextmanager
	def auto_commit(self):
		try:
			yield
			self.session.commit()
		except Exception as e:
			self.session.rollback()
			raise e


# class Query(BaseQuery):
# 	def filter_by(self, **kwargs):
# 		if 'status' not in kwargs.keys():
# 			kwargs['status'] = 1
# 		return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy()


class Base(db.Model):
	__abstract__ = True
	create_time = db.Column('create_time', db.DateTime)
	status = db.Column(db.SmallInteger, default=1)

	def __init__(self):
		self.create_time = datetime.now()

	def set_attrs(self, attrs_dict):
		for k, v in attrs_dict.items():
			# hasattr 某个对象，是否包含某个属性 obj, attr
			if hasattr(self, k) and k != 'id':
				# setattr 对当前对象的某个属性赋值, obj, attr, value
				setattr(self, k, v)
