# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


class LianjiaPipeline(object):
    def process_item(self, item, spider):
        isExists = os.path.exists(item['dir_name'])
        file_name = './' + item['dir_name'] + '/' + item['video_name'] + '.txt'
        if not isExists:
            os.mkdir(item['dir_name'])
        with open(file_name, 'w') as f:
            f.write(item['video_link'])
