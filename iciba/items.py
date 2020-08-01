# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IcibaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class IeltsVocabularyItem(scrapy.Item):
    # 单词
    word = scrapy.Field()
    # 中文释义
    zn_name = scrapy.Field()
    # 音标
    sound_mark = scrapy.Field()
    # 单词发音
    word_mp3 = scrapy.Field()
    # 英文例句
    en_example_0 = scrapy.Field()
    # 英文例句发音
    en_mp3_0 = scrapy.Field()
    # 中文例句
    en_zn_example_0 = scrapy.Field()

    en_example_1 = scrapy.Field()
    en_mp3_1 = scrapy.Field()
    en_zn_example_1 = scrapy.Field()

    en_example_2 = scrapy.Field()
    en_mp3_2 = scrapy.Field()
    en_zn_example_2 = scrapy.Field()
