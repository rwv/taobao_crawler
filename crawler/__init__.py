#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .item import ItemCrawler
from .rate import RateCrawler


class Crawler:
    """
    淘宝商品及评论爬虫

    """
    def __init__(self, keywords, db, timeout=3):
        """
        初始化 Crawler 类

        :param keywords: 搜索的关键词 list，如 ['手机','Phone']
        :param db: 一个 pymongo.MongoClient.db 的实例
        :param timeout: 爬取超时时间, 默认值为 3
        """
        self.keywords = keywords
        self.item = ItemCrawler(self.keywords, db, timeout)
        self.rate = RateCrawler(db, timeout)

    def run(self):
        """
        运行商品及评论爬虫
        """
        self.item.run()
        self.rate.run()
