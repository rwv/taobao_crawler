#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils.config import config
from crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler(config['keywords'])

    menu = [
        ('Item and rate crawler', crawler.run),
        ('Item crawler', crawler.item_crawler),
        ('Rate crawler', crawler.rate_crawler),
        ('exit', exit)
    ]

    print('Please choose the module you want to use:')
    for i in range(len(menu)):
        print('{}. {}'.format(i, menu[i][0]))
    cursor = input()
    menu[cursor][1]()