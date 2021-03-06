# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from Actress.models.es_type import ActressType


class MysqlPipeline(object):
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('HOST'),
            port=crawler.settings.get('PORT'),
            user=crawler.settings.get('USER'),
            password=crawler.settings.get('PASSWORD'),
            database=crawler.settings.get('DATABASE'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                  db=self.database)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        sql = """insert into actress(name, film, tag, date) values(%s, %s, %s, %s)"""
        self.cursor.execute(sql, (item['name'], item['film'], item['tag'], item['date']))
        self.db.commit()
        return item


class ElasticPipeline(object):
    """
    数据存入elasticsearch
    """
    def process_item(self, item, spider):
        # 将 item 转换为 es 数据
        actress = ActressType()
        actress.name = item['name']
        actress.date = item['date']
        actress.tag = item['tag']
        actress.film = item['film']

        actress.save()

        return item
