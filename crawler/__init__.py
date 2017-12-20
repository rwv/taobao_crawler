#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .item import ItemCrawler
from .rate import RateCrawler


class Crawler:
    def __init__(self, keywords, db, timeout=3):
        self.keywords = keywords
        self.item = ItemCrawler(self.keywords, db, timeout)
        self.rate = RateCrawler(db, timeout)

    def run(self):
        self.item.run()
        self.rate.run()
