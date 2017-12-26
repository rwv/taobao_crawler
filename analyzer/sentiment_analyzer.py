#!/usr/bin/env python
# -*- coding:utf-8 -*-

from snownlp import SnowNLP


class SentimentAnalyzer:
    """
    遍历 rates collection, 对当中每个评论进行情感分析，并将其存入 rates_sentiments collection 中。插入数据示例:
    {'item_id': '561319321061', 'rate_id': NumberLong("331495062062"), 'score': 1.00}
    """

    def __init__(self, db):
        """
        :param db: 一个 pymongo.MongoClient.db 的实例
        """
        self.__db = db
        self.__rates_collection = self.__db.rates
        self.__rates_collection.ensure_index('rate_id', unique=True)
        self.__sentiments_collection = self.__db.rates_sentiments
        self.__sentiments_collection.ensure_index('rate_id', unique=True)

    def run(self):
        """
        运行分析器，分析每个评论，插入数据库中
        """
        rates = self.__rates_collection.find({})
        rate_counts = self.__rates_collection.find({}).count()
        count = 0
        for i in rates:
            count += 1
            print('SnowNLP sentiment analyze: ({}/{})'.format(count, rate_counts))
            if self.__sentiments_collection.find({'rate_id': i['rate_id']}).count() == 0:
                data = {
                    'item_id': i['item_id'],
                    'rate_id': i['rate_id'],
                    'score': SnowNLP(i['rate_content']).sentiments  # TODO multiprocessing
                }
                self.__sentiments_collection.insert(data)
                print('Insert into database {}-{}'.format(i['item_id'], i['rate_id']))
