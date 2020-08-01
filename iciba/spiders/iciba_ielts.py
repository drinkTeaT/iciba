from urllib import parse

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from lxml import etree

from iciba.items import IeltsVocabularyItem


class IcibaIeltsSpider(scrapy.Spider):
    name = 'iciba_ielts'
    allowed_domains = ['word.iciba.com']
    start_urls = ['http://word.iciba.com/?action=card']

    def __init__(self, course, class_id):
        self.course = course
        self.class_id = class_id

    def parse(self, response):
        l = ItemLoader(item=IeltsVocabularyItem(), response=response)
        words = l.get_xpath("//div[@class='change-pic cl']")
        for c in words:
            selector = etree.HTML(c)
            l = ItemLoader(item=IeltsVocabularyItem())

            word = selector.xpath("//span[@class='word']/text()")
            l.add_value('word', word[0])

            zn_name = selector.xpath("//*[@class='word_sy']/dd/@title")
            l.add_value('zn_name', zn_name[0])

            sound_mark = selector.xpath("//span[@class='sound']/text()")
            l.add_value("sound_mark", sound_mark[0].replace("\r", "").replace("\n", "").strip())

            word_mp3 = selector.xpath("//a[@class='icon_s2']/@id")
            l.add_value("word_mp3", word_mp3[0])

            # 例句数据
            en_example_0 = selector.xpath("//dd[@class='card_dj_0 ']/text()")
            l.add_value("en_example_0", en_example_0[0].replace("\r", "").replace("\n", "").strip())
            en_mp3_1 = selector.xpath("//dd[@class='card_dj_0 ']/a/@id")
            l.add_value('en_mp3_0', en_mp3_1[0])
            l.add_value('en_zn_example_0', en_example_0[2].replace("\r", "").replace("\n", "").strip())
            print('hello world')
            yield l.load_item()

    def start_requests(self):
        body = {'class_id': self.class_id, "course_id": self.course, "nologin": 0}
        data = parse.urlencode(body)
        temp = {}
        for i in range(0, 20):
            temp['words_checked[]'] = i
            data += "&" + parse.urlencode(temp)
        for url in self.start_urls:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            yield Request(url, method='POST', body=data, headers=headers)
