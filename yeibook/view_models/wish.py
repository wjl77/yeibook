from view_models.book import BookViewModel


class MyWishes:
	def __init__(self, wishes_of_mine, gift_count_list):
		self.wishes = []
		self.__wishes_of_mine = wishes_of_mine
		self.__gift_count_list = gift_count_list
		self.wishes = self.__parse()

	def __parse(self):
		tmp_list = []
		for wish in self.__wishes_of_mine:
			r = self.__matching(wish)
			tmp_list.append(r)
		return tmp_list

	def __matching(self, wish):
		count = 0
		for gift_count in self.__gift_count_list:
			if wish.isbn == gift_count['isbn']:
				count = gift_count['count']
				break
		r = {
			'id': wish.id,
			'book': BookViewModel(wish.wish_book),
			'wishes_count': count
		}

		return r





