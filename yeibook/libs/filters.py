from datetime import datetime
import timeago


def timeago_format(dt):
	now = datetime.now()
	return timeago.format(dt, now, 'zh_CN')


def month_format(s):
	if '月'	in s:
		month_idx = s.index('月')
		s = s.replace(s[month_idx], '个月')
	else:
		s = s
	return s

