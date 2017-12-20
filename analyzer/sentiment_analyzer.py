#!/usr/bin/env python
# -*- coding:utf-8 -*-

from snownlp import SnowNLP


class SnowNlpSentimentAnalyzer:
    """
    遍历 rates collection, 对当中每个评论进行情感分析，并将其存入 rates_sentiments collection 中。
    """

    def __init__(self, db):
        self.db = db
        self.rates_collection = self.db.rates
        self.rates_collection.ensure_index('rate_id', unique=True)
        self.sentiments_collection = self.db.rates_sentiments
        self.sentiments_collection.ensure_index('rate_id', unique=True)

    def run(self):
        rates = self.rates_collection.find({})
        rate_counts = self.rates_collection.find({}).count()
        count = 0
        for i in rates:
            count += 1
            print('SnowNLP sentiment analyze: ({}/{})'.format(count, rate_counts))
            if self.sentiments_collection.find({'rate_id': i['rate_id']}).count() == 0:
                data = {
                    'item_id': i['item_id'],
                    'rate_id': i['rate_id'],
                    'score': SnowNLP(i['rate_content']).sentiments  # TODO multiprocessing
                }
                self.sentiments_collection.insert(data)
                print('Insert into database {}-{}'.format(i['item_id'], i['rate_id']))
