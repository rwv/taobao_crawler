#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime

from utils.utils import *


class SizeInfoAnalyzerWithTime:
    """ 商品尺寸分析器，由 keywords, classifier 生成堆栈图 """

    def __init__(self, keywords, classifiers):
        """
        initialize SizeInfoAnalyzer

        :param keywords: keywords example:
        {
            '小米': ['米', 'mi'],
            '苹果': ['苹果', 'apple', 'iphone'],
            '三星': ['三星', 'samsung'],
            'Vivo': ['vivo'],
            'OPPO': ['oppo'],
            '华为': ['huawei', '华为']
        }
        :param classifiers: classifiers example:
        ['16G', '32G', '64G', '128G', '256G']
        """
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
                            self.rates[k].append(
                                (datetime.strptime(rate_item['rateDate'], '%Y-%m-%d %H:%M:%S'), rate_item['size_info']))
                        break

    def __insert(self, brand_item, classifier, date):
        def check_week_and_insert(year_dict, week, classifier):
            if year_dict.get(week):
                year_dict[week][classifier] = year_dict[week].get(classifier, 0) + 1
            else:
                week_dict = dict()
                week_dict[classifier] = 1
                year_dict[week] = week_dict

        year, week, weekday = date.isocalendar()
        if brand_item.get(year):
            check_week_and_insert(brand_item[year], week, classifier)
        else:
            year_dict = dict()
            brand_item[year] = year_dict
            check_week_and_insert(brand_item[year], week, classifier)

    def __get_value(self, brand, classifier, year, week):
        try:
            return self.rates_count[brand][year][week][classifier]
        except KeyError:
            return 0

    def __count_by_classifier(self):
        self.rates_count = dict()
        # initialize the rates dict
        for k in self.keywords.keys():
            temp_dict = dict()
            self.rates_count[k] = temp_dict

        for k, size_info_list in self.rates.items():
            count = 0
            size_info_len = len(size_info_list)
            for size_info in size_info_list:
                count += 1
                print('{}: count_by_classifier: ({}/{})'.format(k, count, size_info_len))
                for classifier in self.classifiers:
                    if classifier.lower() in size_info[1].lower():
                        self.__insert(self.rates_count[k], classifier, size_info[0])
                        break

    def run(self):
        self.__read_rates_by_brand()
        self.__count_by_classifier()
        for i in self.keywords.keys():
            self.__draw_stacked_pic(i)
