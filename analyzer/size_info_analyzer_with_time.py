#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime

import isoweek
import matplotlib.pyplot as plt


class SizeInfoAnalyzerWithTime:
    """ 商品尺寸分析器，由 keywords, classifier 生成堆栈图 """

    def __init__(self, keywords, classifiers, db):
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
        self.__db = db

    def __read_rates_by_brand(self):
        self.__rates = dict()
        # initialize the sold dict
        for k in self.keywords.keys():
            self.__rates[k] = list()

        items = self.__db.items.find({'is_crawled': True})
        count = 0
        items_len = self.__db.items.count({'is_crawled': True})

        for item in items:
            count += 1
            print('read_rates_by_brand: ({}/{})'.format(count, items_len))
            for k, keywords_list in self.keywords.items():
                for keyword in keywords_list:
                    # if keyword is in the item title.
                    if keyword in item['title'].lower():
                        # find rate via item_id
                        for rate_item in self.__db.rates.find({'item_id': item['item_id']}):
                            self.__rates[k].append(
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
            return self.__rates_count[brand][year][week][classifier]
        except KeyError:
            return 0

    def __count_by_classifier(self):
        self.__rates_count = dict()
        # initialize the sold dict
        for k in self.keywords.keys():
            temp_dict = dict()
            self.__rates_count[k] = temp_dict

        for k, size_info_list in self.__rates.items():
            count = 0
            size_info_len = len(size_info_list)
            for size_info in size_info_list:
                count += 1
                print('{}: count_by_classifier: ({}/{})'.format(k, count, size_info_len))
                for classifier in self.classifiers:
                    if classifier.lower() in size_info[1].lower():
                        self.__insert(self.__rates_count[k], classifier, size_info[0])
                        break

    def __draw_stack_chart(self, brand):
        # handle the data
        data = self.__rates_count[brand]
        years_weeks = list()
        for key, values in data.items():
            for value in values.keys():
                years_weeks.append(isoweek.Week(key, value))
        years_weeks = sorted(years_weeks)  # a year have 53 weeks at most
        count_by_time = dict()
        for classifier in self.classifiers:
            temp = list()
            count_by_time[classifier] = temp
        for year_week in years_weeks:
            for classifier in self.classifiers:
                count_by_time[classifier].append(self.__get_value(brand, classifier, year_week.year, year_week.week))

        # draw the pic
        axis_label = years_weeks.copy()
        min_week = isoweek.Week(min(years_weeks).year, 0)
        years_weeks = list(map(lambda x: x - min_week, years_weeks))
        count = list()
        labels = list()
        for k, v in count_by_time.items():
            count.append(v)
            labels.append(k)

        axis_label = list(map(lambda x: x.week, axis_label))

        # convert the sum of sold number to 1
        for j in range(len(count[0])):
            s = 0
            for i in range(len(count)):
                s += count[i][j]
            for i in range(len(count)):
                count[i][j] /= s

        plt.figure(figsize=(15, 5))
        plt.style.use('ggplot')
        plt.stackplot(years_weeks, count, labels=labels)
        plt.legend(loc='best')
        plt.tick_params(top='off', right='off')
        plt.xticks(years_weeks[::int(len(axis_label) / 15)], axis_label[::int(len(axis_label) / 15)])
        plt.savefig('size_info_analyzer_with_time_{}.pdf'.format(brand))

    def run(self):
        self.__read_rates_by_brand()
        self.__count_by_classifier()
        for i in self.keywords.keys():
            self.__draw_stack_chart(i)
