

class TradeInfo:
	def __init__(self, goods):
		self.total = 0
		self.trades = []
		self.__parse(goods)

	def __parse(self, goods):
		self.total = len(goods)
		self.trades = [self.__map_to_trade(single) for single in goods]

	def __map_to_trade(self, single):
		return dict(
			user_head=single.user.user_head,
			user_name=single.user.nickname,
			time=single.create_time.strftime('%Y-%m-%d'),
			id=single.id
		)
