# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanBooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    detail_url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    info = scrapy.Field()
    isbn = scrapy.Field()
    rating = scrapy.Field()
    intro = scrapy.Field()
    img = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    img_url = scrapy.Field()
    pub_date = scrapy.Field()

