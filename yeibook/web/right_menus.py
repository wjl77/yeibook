from sqlalchemy import func, desc
from gather.ye_book import YeBook
from models.base import db
from models.gift import Gift
from models.user import User
from models.wish import Wish
# 最受欢迎赠书者
popular_gifters_list = []
popular_gifters = db.session.query(
	Gift.uid, func.count(Gift.id)).filter(Gift.status == 1, Gift.launched == 0).group_by(
	Gift.uid).order_by(desc(func.count(Gift.id))).limit(10).all()

for popular_gifter in popular_gifters:
	tmp_data = {}
	user = User.query.get(popular_gifter[0])
	count = popular_gifter[1]
	tmp_data['nickname'] = user.nickname
	tmp_data['count'] = count
	popular_gifters_list.append(tmp_data)
# print(popular_gifters_list)
# 最受欢迎心愿
popular_wishes_list = []
popular_wishes = db.session.query(Wish.isbn, func.count(Wish.id)).filter(
	Wish.status == 1, Wish.launched == 0).group_by(
	Wish.isbn).order_by(desc(func.count(Wish.id))).limit(5).all()
# print(popular_wishes)

for popular_wish in popular_wishes:
	ye_book = YeBook()
	tmp_data = {}
	ye_book.search_by_isbn(popular_wish[0])
	wish_title = ye_book.first['title']
	count = popular_wish[1]
	tmp_data['count'] = count
	tmp_data['wish_title'] = wish_title
	popular_wishes_list.append(tmp_data)
