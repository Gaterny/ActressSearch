#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date, Keyword, Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

# 创建连接
connections.create_connection(hosts=['localhost'])


class CustomAnalyzer(_CustomAnalyzer):
    """
    自动补全
    """
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer('ik_max_word', filter=['lowercase'])


class ActressType(Document):
    """
    类型配置
    """
    suggest = Completion(analyzer=ik_analyzer)
    name = Text(analyzer='ik_max_word') # 分词
    date = Date()
    film = Text(analyzer='ik_max_word')
    tag = Keyword()

    class Index:
        name = 'actress'
        settings = {
            'number_of_shards': 2,
        }


if __name__ == "__main__":
    ActressType.init()