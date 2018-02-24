# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import json

from lianjia.items import LianjiaItem
from lianjia.settings import *

from PIL import Image


class VideoSpiderSpider(scrapy.Spider):
    name = 'video_spider'
    start_urls = ['http://www.ljabc.com.cn/user/toUserLogin.html']
    course_urls = ['http://www.ljabc.com.cn/user/toCourseDetail.html?courseId=691604']

    def parse(self, response):
        captcha_url = 'http://www.ljabc.com.cn/user/loginCaptcha.html'
        yield scrapy.Request(url=captcha_url,
                             callback=self.parser_captcha)

    def parser_captcha(self, response):
        login_url = 'http://www.ljabc.com.cn/user/userLoginByAjax.html'

        def get_captcha(response):
            with open('captcha.jpg', 'wb') as f:
                f.write(response.body)
                f.close()
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
            captcha = input("input the captcha\n>")
            return captcha

        formdata = {
            'phone': USER_NAME,
            'password': USER_PASSWORD,
            'captcha': get_captcha(response),
            'roleMark': '',
        }

        yield scrapy.FormRequest(
            url=login_url,
            formdata=formdata,
            callback=self.after_login
        )

    def after_login(self, response):
        if response.text == '1':
            print('login succeeded')
            for course_url in self.course_urls:

                yield scrapy.Request(
                    url=course_url,
                    callback=self.get_courseid
                )

    def get_courseid(self, response):
        video_url = 'http://www.ljabc.com.cn/system/getCourseVideosByCourseId.html'
        re_c = re.compile(r'courseId=(\d+)')
        searched = re_c.search(response.url)
        if searched:
            course_id = searched.group(1)
            yield scrapy.FormRequest(
                url=video_url,
                formdata={'courseId':course_id},
                callback=self.down_loader
            )

    def down_loader(self, response):
        item = LianjiaItem()
        video_list = json.loads(response.text)
        for video in video_list:
            item['video_link'] = video['HPVD_PATH']
            item['video_name'] = video['HPVD_DESCR']
            item['dir_name'] = video['HPCO_NAME']
            yield item


# des(key, message, encrypt, mode, iv, padding)
# des(genKey.key, input, 1, 1, des3iv, 1)
if __name__ == '__main__':
    from pyDes import *
    key = 'zhangxl1235@lx100$#365#$'
    data = "Ax"
    for i in range(len(key), 24):
        key += '0'
    k = triple_des(key, CBC, IV='zhangxl6', pad=None, padmode=PAD_PKCS5)
    d = k.encrypt(data)
