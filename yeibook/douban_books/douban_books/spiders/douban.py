# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from douban_books.items import DoubanBooksItem
# https://book.douban.com/tag/%E9%9A%8F%E7%AC%94?start=20&type=T

# from douban_books.douban_books.items import DoubanBooksItem

## 小说 https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4 966
## 编程 https://book.douban.com/tag/%E7%BC%96%E7%A8%8B 851
## 隋笔 https://book.douban.com/tag/%E9%9A%8F%E7%AC%94 951
## 散文 https://book.douban.com/tag/%E6%95%A3%E6%96%87 483
## 诗歌 https://book.douban.com/tag/%E8%AF%97%E6%AD%8C 832
## 日本文学 https://book.douban.com/tag/%E6%97%A5%E6%9C%AC%E6%96%87%E5%AD%A6 692
## 外国文学 https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6 429
## 商业 https://book.douban.com/tag/%E5%95%86%E4%B8%9A 819
## 中国文学 https://book.douban.com/tag/%E4%B8%AD%E5%9B%BD%E6%96%87%E5%AD%A6 496
## 漫画 https://book.douban.com/tag/%E6%BC%AB%E7%94%BB 735
## 历史 https://book.douban.com/tag/%E5%8E%86%E5%8F%B2 781
## 网络小说 https://book.douban.com/tag/%E7%BD%91%E7%BB%9C%E5%B0%8F%E8%AF%B4 797
## 名著 https://book.douban.com/tag/%E5%90%8D%E8%91%97 609
## 经济学 https://book.douban.com/tag/%E7%BB%8F%E6%B5%8E%E5%AD%A6 408
## 旅行 https://book.douban.com/tag/%E6%97%85%E8%A1%8C 684
## 美食 https://book.douban.com/tag/%E7%BE%8E%E9%A3%9F 730
## 金融 https://book.douban.com/tag/%E9%87%91%E8%9E%8D 530
## 科幻 https://book.douban.com/tag/%E7%A7%91%E5%B9%BB 409
## 安妮宝贝 https://book.douban.com/tag/%E5%AE%89%E5%A6%AE%E5%AE%9D%E8%B4%9D 149
## 科幻小说 https://book.douban.com/tag/%E7%A7%91%E5%B9%BB%E5%B0%8F%E8%AF%B4 618
## 推理小说 https://book.douban.com/tag/%E6%8E%A8%E7%90%86%E5%B0%8F%E8%AF%B4 582
## 东野圭吾 https://book.douban.com/tag/%E4%B8%9C%E9%87%8E%E5%9C%AD%E5%90%BE 353
## 文学 https://book.douban.com/tag/%E6%96%87%E5%AD%A6 62
## 哲学 https://book.douban.com/tag/%E5%93%B2%E5%AD%A6 577
## 摄影 https://book.douban.com/tag/%E6%91%84%E5%BD%B1 714
## 设计 https://book.douban.com/tag/%E8%AE%BE%E8%AE%A1 407
## 艺术 https://book.douban.com/tag/%E8%89%BA%E6%9C%AF 410
## 美术 https://book.douban.com/tag/%E7%BE%8E%E6%9C%AF 515
## 电影 https://book.douban.com/tag/%E7%94%B5%E5%BD%B1 606
## 文化 https://book.douban.com/tag/%E6%96%87%E5%8C%96 120
## 青春文学 https://book.douban.com/tag/%E9%9D%92%E6%98%A5%E6%96%87%E5%AD%A6 606
## 科普 https://book.douban.com/tag/%E7%A7%91%E6%99%AE 509
## 经典 https://book.douban.com/tag/%E7%BB%8F%E5%85%B8 133
## 音乐 https://book.douban.com/tag/%E9%9F%B3%E4%B9%90 739
## 奇幻 https://book.douban.com/tag/%E5%A5%87%E5%B9%BB 535
## 绘画 https://book.douban.com/tag/%E7%BB%98%E7%94%BB 623

# 推理 https://book.douban.com/tag/%E6%8E%A8%E7%90%86 134
# 悬疑 https://book.douban.com/tag/%E6%82%AC%E7%96%91 283
# 管理 https://book.douban.com/tag/%E7%AE%A1%E7%90%86 539
# 营销 https://book.douban.com/tag/%E8%90%A5%E9%94%80 643
# 投资 https://book.douban.com/tag/%E6%8A%95%E8%B5%84 283
# 言情 https://book.douban.com/tag/%E8%A8%80%E6%83%85 476
# 儿童文学 https://book.douban.com/tag/%E5%84%BF%E7%AB%A5%E6%96%87%E5%AD%A6 723
# 武侠 https://book.douban.com/tag/%E6%AD%A6%E4%BE%A0 568
# 国学 https://book.douban.com/tag/%E5%9B%BD%E5%AD%A6 522
# 心理学 https://book.douban.com/tag/%E5%BF%83%E7%90%86%E5%AD%A6 563
# 中国历史 https://book.douban.com/tag/%E4%B8%AD%E5%9B%BD%E5%8E%86%E5%8F%B2 623
# 社会学 https://book.douban.com/tag/%E7%A4%BE%E4%BC%9A%E5%AD%A6 449
# 思想 https://book.douban.com/tag/%E6%80%9D%E6%83%B3 532
# 手工 https://book.douban.com/tag/%E6%89%8B%E5%B7%A5 491
# 情感 https://book.douban.com/tag/%E6%83%85%E6%84%9F 41
# 养生 https://book.douban.com/tag/%E5%85%BB%E7%94%9F 593
# 自助游 https://book.douban.com/tag/%E8%87%AA%E5%8A%A9%E6%B8%B8 181
# 职场 https://book.douban.com/tag/%E8%81%8C%E5%9C%BA 608
# 互联网 https://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91 465
# 科学 https://book.douban.com/tag/%E7%A7%91%E5%AD%A6 582
# 交互设计 https://book.douban.com/tag/%E4%BA%A4%E4%BA%92%E8%AE%BE%E8%AE%A1 447
# 考古 https://book.douban.com/tag/%E8%80%83%E5%8F%A4 681
# 算法 https://book.douban.com/tag/%E7%AE%97%E6%B3%95 493
# 耽美 https://book.douban.com/tag/%E8%80%BD%E7%BE%8E 501
# 用户体验 https://book.douban.com/tag/%E7%94%A8%E6%88%B7%E4%BD%93%E9%AA%8C 163
# 科技 https://book.douban.com/tag/%E7%A7%91%E6%8A%80 384
# web https://book.douban.com/tag/web 309
# 经济 https://book.douban.com/tag/%E7%BB%8F%E6%B5%8E 306
# 西方哲学 https://book.douban.com/tag/%E8%A5%BF%E6%96%B9%E5%93%B2%E5%AD%A6 627
# 古典文学 https://book.douban.com/tag/%E5%8F%A4%E5%85%B8%E6%96%87%E5%AD%A6 568
# 当代文学 https://book.douban.com/tag/%E5%BD%93%E4%BB%A3%E6%96%87%E5%AD%A6 547
# 建筑 https://book.douban.com/tag/%E5%BB%BA%E7%AD%91 638
# 生活 https://book.douban.com/tag/%E7%94%9F%E6%B4%BB 357
# 励志 https://book.douban.com/tag/%E5%8A%B1%E5%BF%97 566
# 爱情 https://book.douban.com/tag/%E7%88%B1%E6%83%85 245

# 阿加莎·克里斯蒂 https://book.douban.com/tag/%E9%98%BF%E5%8A%A0%E8%8E%8E%C2%B7%E5%85%8B%E9%87%8C%E6%96%AF%E8%92%82 383
# 魔幻 https://book.douban.com/tag/%E9%AD%94%E5%B9%BB 374
# 杂文 https://book.douban.com/tag/%E6%9D%82%E6%96%87 504
# 诗词 https://book.douban.com/tag/%E8%AF%97%E8%AF%8D 495
# 外国名著 https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E5%90%8D%E8%91%97 284
# 港台 https://book.douban.com/tag/%E6%B8%AF%E5%8F%B0 304
# 绘本 https://book.douban.com/tag/%E7%BB%98%E6%9C%AC 468
# 青春 https://book.douban.com/tag/%E9%9D%92%E6%98%A5 353
# 日本漫画 https://book.douban.com/tag/%E6%97%A5%E6%9C%AC%E6%BC%AB%E7%94%BB 305
# 三毛 https://book.douban.com/tag/%E4%B8%89%E6%AF%9B 291
# 轻小说 https://book.douban.com/tag/%E8%BD%BB%E5%B0%8F%E8%AF%B4 616
# 校园 https://book.douban.com/tag/%E6%A0%A1%E5%9B%AD 368
# 传记 https://book.douban.com/tag/%E4%BC%A0%E8%AE%B0 390
# 社会 https://book.douban.com/tag/%E7%A4%BE%E4%BC%9A 247
# 政治 https://book.douban.com/tag/%E6%94%BF%E6%B2%BB 371
# 政治学 https://book.douban.com/tag/%E6%94%BF%E6%B2%BB%E5%AD%A6 351
# 宗教 https://book.douban.com/tag/%E5%AE%97%E6%95%99 594
# 数学 https://book.douban.com/tag/%E6%95%B0%E5%AD%A6 599
# 回忆录 https://book.douban.com/tag/%E5%9B%9E%E5%BF%86%E5%BD%95 492
# 人物传记 https://book.douban.com/tag/%E4%BA%BA%E7%89%A9%E4%BC%A0%E8%AE%B0 414
# 创业 https://book.douban.com/tag/%E5%88%9B%E4%B8%9A 343
# 广告 https://book.douban.com/tag/%E5%B9%BF%E5%91%8A 418
# 策划 https://book.douban.com/tag/%E7%AD%96%E5%88%92 370
# 企业史 https://book.douban.com/tag/%E4%BC%81%E4%B8%9A%E5%8F%B2 259
# 股票 https://book.douban.com/tag/%E8%82%A1%E7%A5%A8 246
# 人文 https://book.douban.com/tag/%E4%BA%BA%E6%96%87 434
# 家居 https://book.douban.com/tag/%E5%AE%B6%E5%B1%85 431
# 戏剧 https://book.douban.com/tag/%E6%88%8F%E5%89%A7 592
# 近代史 https://book.douban.com/tag/%E8%BF%91%E4%BB%A3%E5%8F%B2 563
# 二战 https://book.douban.com/tag/%E4%BA%8C%E6%88%98 426
# 军事 https://book.douban.com/tag/%E5%86%9B%E4%BA%8B 549
# 健康 https://book.douban.com/tag/%E5%81%A5%E5%BA%B7 531
# 游记 https://book.douban.com/tag/%E6%B8%B8%E8%AE%B0 452
# 佛教 https://book.douban.com/tag/%E4%BD%9B%E6%95%99 83
# 教育 https://book.douban.com/tag/%E6%95%99%E8%82%B2 577
# 成长 https://book.douban.com/tag/%E6%88%90%E9%95%BF 149
# 人际关系 https://book.douban.com/tag/%E4%BA%BA%E9%99%85%E5%85%B3%E7%B3%BB 388
# 自由主义 https://book.douban.com/tag/%E8%87%AA%E7%94%B1%E4%B8%BB%E4%B9%89 299
# 理财 https://book.douban.com/tag/%E7%90%86%E8%B4%A2 366
# 艺术史 https://book.douban.com/tag/%E8%89%BA%E6%9C%AF%E5%8F%B2 353
# 灵修 https://book.douban.com/tag/%E7%81%B5%E4%BF%AE 487
# 通信 https://book.douban.com/tag/%E9%80%9A%E4%BF%A1 461
# 交互 https://book.douban.com/tag/%E4%BA%A4%E4%BA%92 85
# 神经网络 https://book.douban.com/tag/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C 130
# 两性 https://book.douban.com/tag/%E4%B8%A4%E6%80%A7 448
# 程序 https://book.douban.com/tag/%E7%A8%8B%E5%BA%8F 142
# UE https://book.douban.com/tag/UE 28
# UCD https://book.douban.com/tag/UCD 34
# 张爱玲 https://book.douban.com/tag/%E5%BC%A0%E7%88%B1%E7%8E%B2 370

#######################

#######################


class DoubanSpider(scrapy.Spider):
    current_start = 0
    name = 'douban'
    # allowed_domains = ['book.douban.com']
    start_url = 'https://book.douban.com/tag/%E9%9A%8F%E7%AC%94?start={}&type=T'.format(current_start)
    # header = {
    #     'Referer': 'http://www.baidu.com'
    # }

    def start_requests(self):
        yield scrapy.Request(url=self.start_url,
                             callback=self.parse)

    def parse(self, response):
        meta = {}
        for detail_item in response.xpath('//ul[@class="subject-list"]/li'):
            meta['category'] = response.xpath('//div[@id="content"]/h1/text()').extract_first().split(':')[-1].strip()
            meta['title'] = detail_item.xpath('.//h2/a/@title').extract_first()
            meta['author'] = detail_item.xpath('.//div[@class="pub"]/text()').extract_first().strip().split(' / ')[0]
            meta['info'] = ' / '.join(detail_item.xpath('.//div[@class="pub"]/text()').extract_first().strip().split(' / ')[:-1])
            meta['price'] = detail_item.xpath('.//div[@class="pub"]/text()').extract_first().strip().split(' / ')[-1]
            meta['intro'] = detail_item.xpath('.//p/text()').extract_first()
            meta['rating'] = detail_item.xpath('.//span[@class="rating_nums"]/text()').extract_first()
            meta['img_url'] = detail_item.xpath('.//a[@class="nbg"]/img/@src').extract_first()
            meta['detail_url'] = detail_item.xpath('.//h2/a/@href').extract_first()
            yield scrapy.Request(url=meta['detail_url'],
                                 callback=self.parse_detail,
                                 meta=meta)

        self.current_start += 20
        if self.current_start <= 980:
            next_url = 'https://book.douban.com/tag/%E9%9A%8F%E7%AC%94?start={}&type=T'.format(self.current_start)
            yield scrapy.Request(url=next_url,
                                 callback=self.parse)

    def parse_detail(self, response):
        date_str = response.meta['info'].split('/')[-1].strip()
        date = date_str.split('-')[0] + '-' + date_str.split('-')[1]
        item = DoubanBooksItem()
        item['category'] = response.meta['category']
        item['title'] = response.meta['title']
        item['author'] = response.meta['author']
        item['info'] = response.meta['info']
        item['intro'] = response.meta['intro'].replace('\n', '')
        item['rating'] = response.meta['rating']
        item['img_url'] = response.meta['img_url']
        item['image_urls'] = [response.meta['img_url']]
        item['isbn'] = response.xpath('//div[@id="info"]/text()').extract()[-2].strip()
        item['price'] = response.meta['price']
        item['img'] = response.meta['img_url'].split('/')[-1]
        item['pub_date'] = datetime.strptime(date, '%Y-%m').strftime('%Y-%m')
        yield item



