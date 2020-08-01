# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import traceback

import dj_database_url
from scrapy.exceptions import NotConfigured
from twisted.enterprise import adbapi
from twisted.internet import defer


class IcibaPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        mysql_url = crawler.settings.get('MYSQL_PIPELINE_URL', None)
        if not mysql_url:
            raise NotConfigured
        return cls(mysql_url)

    def __init__(self, mysql_url):
        conn_kwargs = IcibaPipeline.parse_mysql_url(mysql_url)
        self.dbpool = adbapi.ConnectionPool('pymysql', charset='utf8', use_unicode=True, connect_timeout=5,
                                            **conn_kwargs)

    def close_spider(self, spider):
        return
        self.dbpool.close()

    # noinspection PyBroadException
    @defer.inlineCallbacks
    def process_item(self, item, spider):
        try:
            yield self.dbpool.runInteraction(self.do_insert, item)
        except:
            print(traceback.format_exc())
        defer.returnValue(item)

    @staticmethod
    def parse_mysql_url(mysql_url):
        params = dj_database_url.parse(mysql_url)
        conn_kwargs = {}
        conn_kwargs['host'] = params['HOST']
        conn_kwargs['user'] = params['USER']
        conn_kwargs['passwd'] = params['PASSWORD']
        conn_kwargs['db'] = params['NAME']
        conn_kwargs['port'] = params['PORT']
        return conn_kwargs

    @staticmethod
    def do_insert(tx, item):
        if IcibaPipeline.do_query(tx, item) > 0:
            return
        sql = """INSERT INTO  t_iciba_ielts (WORD,ZNNAME,	WORDMP3,SOUNDMARK,ENEXAMPLE,ENEXAMPLEMP3,ZNEXAMPLE)	VALUES	(%s,%s,%s,%s,%s,%s,%s)"""
        args = (
            item["word"][0],
            item["zn_name"][0], item["word_mp3"][0], item["sound_mark"][0], item["en_example_0"][0],
            item["en_mp3_0"][0],
            item["en_zn_example_0"][0])
        tx.execute(sql, args)

    @staticmethod
    def do_query(tx, item):
        sql = """SELECT ID FROM t_iciba_ielts WHERE WORD = %s """
        args = (
            item["word"][0])
        result = tx.execute(sql, args)
        return result
