from enum import Enum


class PendingStatus(Enum):
	Wating = 1
	Success = 2
	Reject = 3
	Redraw = 4

	@classmethod
	def pending_str(cls, status, key):
		key_map = {
			cls.Wating: {
				'requester': '等待对方邮寄',
				'gifter': '等待你邮寄'
			},
			cls.Reject: {
				'requester': '对方已拒绝',
				'gifter': '你已拒绝'
			},
			cls.Redraw: {
				'requester': '你已撤销',
				'gifter': '对方已撤销'
			},
			cls.Success: {
				'requester': '对方已邮寄',
				'gifter': '你已邮寄'
			}
		}

		return key_map[status][key]