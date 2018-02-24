# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    video_link = scrapy.Field()
    video_name = scrapy.Field()
    dir_name = scrapy.Field()