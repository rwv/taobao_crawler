#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

sys.path.append("../")
from utils.utils import *

reload(sys)
sys.setdefaultencoding('utf8')


class SizeInfoAnalyzer:
    """ 爬取淘宝手机商品记录 """

    def __init__(self, keywords, classifiers):
        keywords = {
            '小米': ['米', 'mi'],
            '苹果': ['苹果', 'apple', 'iphone'],
            '三星': ['三星', 'samsung'],
            'Vivo': ['vivo'],
            'OPPO': ['oppo'],
            '华为': ['huawei', '华为']
        }
        classifiers = ['16G', '32G', '64G', '128G', '256G']

        self.keywords = keywords
        self.classifiers = classifiers
        self.client, self.db = init_client()

    def __read_rates_by_brand(self):
        self.rates = dict()
        # initialize the rates dict
        for k in self.keywords.keys():
            self.rates[k] = list()

        items = self.db.items.find({'is_crawled': True})
        count = 0
        items_len = self.db.items.count({'is_crawled': True})

        for item in items:
            count += 1
            print('read_rates_by_brand: ({}/{})'.format(count, items_len))
            for k, keywords_list in self.keywords.items():
                for keyword in keywords_list:
                    # if keyword is in the item title.
                    if keyword in item['title'].lower():
                        # find rate via item_id
                        for rate_item in self.db.rates.find({'item_id': item['item_id']}):
                            self.rates[k].append(rate_item['size_info'])
                        break

    def __count_by_classifier(self):
        self.rates_count = dict()
        # initialize the rates dict
        for k in self.keywords.keys():
            temp_dict = dict()
            for classifier in self.classifiers:
                temp_dict[classifier] = 0
            self.rates_count[k] = temp_dict

        for k, size_info_list in self.rates.items():
            count = 0
            size_info_len = len(size_info_list)
            for size_info in size_info_list:
                count += 1
                print('{}: count_by_classifier: ({}/{})'.format(k, count, size_info_len))
                for classifier in self.classifiers:
                    if classifier.lower() in size_info.lower():
                        self.rates_count[k][classifier] += 1
                        break

    def run(self):
        self.__read_rates_by_brand()
        self.__count_by_classifier()
        print(self.rates_count)
