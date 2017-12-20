#!/usr/bin/env python
# -*- coding:utf-8 -*-


import matplotlib.pyplot as plt
from numpy import ceil, floor


class SoldNumberAnalyzer:
    """ 商品销量分析器，由 keywords, 价格生成堆栈图 """

    def __init__(self, keywords, db):
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
        """
        self.keywords = keywords
        self.__db = db

    def __count_by_price(self):
        self.__sold = dict()
        # initialize the sold dict
        for k in self.keywords.keys():
            self.__sold[k] = dict()

        items = list(self.__db.items.find({'is_crawled': True}))
        count = 0
        items_len = self.__db.items.count({'is_crawled': True})

        for item in items:
            count += 1
            print('read_rates_by_brand: ({}/{})'.format(count, items_len))
            for brand, keywords_list in self.keywords.items():
                for keyword in keywords_list:
                    # if keyword is in the item title.
                    if keyword in item['title'].lower():
                        # find rate via item_id
                        self.__sold[brand][float(item['price'])] = self.__sold[brand].get(float(item['price']),
                                                                                          0) + self.__db.rates.count(
                            {'item_id': item['item_id']})
        print(self.__sold)

    def __get_sold(self, lower, upper, brand):
        data = self.__sold[brand]
        sum = 0
        for price, count in data.items():
            if lower <= price < upper:
                sum += count
        return sum

    def __draw_stack_chart(self, div=10):
        prices_list = []
        for i in self.__sold.values():
            for j in i.keys():
                prices_list.append(j)
        min_price = int(floor(min(prices_list)))
        max_price = int(ceil(max(prices_list)))

        # generate the price sequence from max price and min price
        prices_seq = list(range(min_price, max_price, int((max_price - min_price) / div)))
        if prices_seq[-1] != max_price:
            prices_seq.append(max_price)

        # generate the related sold list
        temp = prices_seq.copy()
        temp.append(max_price + 1)
        brands = list(self.keywords.keys())
        counts = []
        for brand in brands:
            temp_list = list()
            for i in range(len(temp) - 1):
                temp_list.append(self.__get_sold(temp[i], temp[i + 1], brand))
            counts.append(temp_list)

        plt.figure(figsize=(15, 5))
        plt.style.use('ggplot')
        plt.stackplot(prices_seq, counts, labels=brands)
        plt.legend(loc='best')
        plt.tick_params(top='off', right='off')
        plt.savefig('sold_number_analyzer.pdf')

    def run(self):
        self.__count_by_price()
        self.__draw_stack_chart()
