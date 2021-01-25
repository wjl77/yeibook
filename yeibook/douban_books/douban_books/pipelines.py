# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class DoubanBooksPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline:
    def __init__(self):
        self.title_set = set()

    def process_item(self, item, spider):
        if item['title'] in self.title_set:
            raise DropItem('重复的书名: {}'.format(item))
        self.title_set.add(item['title'])
        return item


class DouBanImagesPipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('image does not exist')
        return item

    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name


class MySQLPipeline:
    def __init__(self):
        self.db_conn = MySQLdb.connect(db='fishbook',
                                       host='localhost',
                                       user='root',
                                       password='sys12091',
                                       charset='utf8')
        self.db_cursor = self.db_conn.cursor()

    def process_item(self, item, spider):
        values = (item['category'],
                  item['title'],
                  item['author'],
                  item['info'],
                  item['intro'],
                  item['rating'],
                  item['img_url'],
                  item['isbn'],
                  item['price'],
                  item['img'],
                  item['pub_date'])
        sql = 'insert into book(category, title, author, info, intro, rating, img_url, isbn, price, img, pub_date)' \
              'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.db_cursor.execute(sql, values)
        return item

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_cursor.close()
        self.db_conn.close()

