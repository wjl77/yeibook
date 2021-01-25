from view_models.book import BookViewModel


class MyGifts:
	def __init__(self, gifts_of_mine, wish_count_list):
		self.gifts = []
		self.__gifts_of_mine = gifts_of_mine
		self.__wish_count_list = wish_count_list
		self.gifts = self.__parse()

	def __parse(self):
		tmp_list = []
		for gift in self.__gifts_of_mine:
			r = self.__matching(gift)
			tmp_list.append(r)
		return tmp_list

	def __matching(self, gift):
		count = 0
		for wish_count in self.__wish_count_list:
			if gift.isbn == wish_count['isbn']:
				count = wish_count['count']
				break
		r = {
			'id': gift.id,
			'book': BookViewModel(gift.gift_book),
			'wishes_count': count
		}

		return r





