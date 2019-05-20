# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题
    raw_title = scrapy.Field()
    # 图片地址
    pic_url = scrapy.Field()
    # 详情页地址
    detail_url = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 店铺地址
    loc = scrapy.Field()
    # 销量
    sales = scrapy.Field()
    shop = scrapy.Field()


