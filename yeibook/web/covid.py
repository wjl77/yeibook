import hashlib
from datetime import datetime
import requests
from flask import render_template, jsonify

from web.blueprint import web


@web.route('/covid19')
def covid19():
	current_date = datetime.now().strftime('%Y-%m-%d')
	return render_template('covid19.html', current_date=current_date)


@web.route('/covid19/china', methods=['GET', 'POST'])
def covid19_china():
	appid = '5374'
	sign = 'a28968b5b18c26aab5e63168cfa26295'
	china_url = 'https://vyps.api.storeapi.net/api/94/219'
	r = requests.get(f'{china_url}?appid={appid}&sign={sign}')
	province_list = []
	if r:
		result = r.json()
		result_list = result['retdata']

		for result_item in result_list:
			item_data = {}
			item_data['province'] = result_item['xArea']
			# 当前确诊
			item_data['curConfirm'] = result_item['curConfirm']
			item_data['confirm'] = result_item['confirm']
			item_data['died'] = result_item['died']
			item_data['heal'] = result_item['heal']
			province_list.append(item_data)

		province_rank_list = []
		tmp_list = []
		for province in province_list:
			tmp_list.append(int(province['curConfirm']))

		tmp_sorted_list = sorted(tmp_list, reverse=True)

		for tmp_sorted_num in tmp_sorted_list:
			for province in province_list:
				if tmp_sorted_num == int(province['curConfirm']):
					province_rank_list.append(province)

		returned_data = {
			'code': 0,
			'data': province_rank_list[:10][::-1]
		}
		return jsonify(returned_data)
	return jsonify({})


@web.route('/covid19/global', methods=['GET', 'POST'])
def covid19_global():
	# raw = 'appid53743f5b6bc5ff4a031fb3abe0a4107e04e4'
	# s = hashlib.md5(raw.encode()).hexdigest()
	# print(s)
	appid = '5374'
	sign = 'a28968b5b18c26aab5e63168cfa26295'
	global_url = 'https://vyps.api.storeapi.net/api/94/222'
	r = requests.get(f'{global_url}?appid={appid}&sign={sign}')
	if r:
		result = r.json()
		nation_top_10 = [{'country_name': country['xName'], 'avg_confirm': country['xValue']} for country in
						 result['retdata']['topAddCountry']]
		nation_list = []
		global_rank_list = []

		for sublist in result['retdata']['globalList']:
			if sublist['xArea'] != '热门':
				for subitem in sublist['subList']:
					for country in nation_top_10:
						item_data = {}
						if country['country_name'] == subitem['country']:
							item_data['country'] = subitem['country']
							item_data['confirm'] = subitem['confirm']
							item_data['curConfirm'] = subitem['curConfirm']
							item_data['died'] = subitem['died']
							item_data['avg_confirm'] = country['avg_confirm']
							nation_list.append(item_data)

		for country_item in nation_top_10:
			for country in nation_list:
				item = {}
				if country_item['country_name'] == country['country']:
					item['country'] = country['country']
					item['curConfirm'] = country['curConfirm']
					item['confirm'] = country['confirm']
					item['died'] = country['died']
					item['avg_confirm'] = country['avg_confirm']
					global_rank_list.append(item)

		returned_data = {
			'code': 0,
			'data': global_rank_list[::-1]
		}

		return jsonify(returned_data)

	returned_data = {
		'code': 1,
		'data': {}
	}
	return jsonify(returned_data)

