#!/usr/bin/env python
# -*- coding:utf-8 -*-

from item import ItemCrawler
from rate import RateCrawler


class Crawler:
    def __init__(self, keywords):
        self.item_crawler = ItemCrawler(keywords)
        self.rate_crawler = RateCrawler()

    def run(self):
        """
        run the item and rate crawler
        """
        self.item_crawler.run()
        self.rate_crawler.run()

    def run_item_crawler(self):
        """
        run the item crawler
        """
        self.item_crawler.run()

    def run_rate_crawler(self):
        """
        run the rate crawler
        """
        self.rate_crawler.run()
