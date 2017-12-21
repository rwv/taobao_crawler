#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
from numpy import sqrt, ceil, floor


class SizeInfoAnalyzer:
    """
    商品尺寸分析器，由关键词，分类器生成饼状图
    """

    def __init__(self, keywords, classifiers, db):
        """
        :param keywords: 一个关键词的字典, 关键词的值为一个包含可能的, 示例:
         {'小米': ['米', 'mi'], '苹果': ['苹果', 'apple', 'iphone']}
        :param classifiers: 一个分类器的列表, 示例:
         ['16G', '32G', '64G', '128G', '256G']
        :param db: 一个 pymongo.MongoClient.db 的实例
        """
        self.keywords = keywords
        self.classifiers = classifiers
        self.__db = db

    def __read_rates_by_brand(self):
        """
        读取各个品牌商品所有评论的商品尺寸信息，存储至 self.__rates 中。
        """
        self.__rates = dict()
        # initialize the rates dict
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
                            self.__rates[k].append(rate_item['size_info'])
                        break

    def __count_by_classifier(self):
        """
        通过分类器对所有商品尺寸信息进行分类，计数。
        """
        self.__rates_count = dict()
        # initialize the rates dict
        for k in self.keywords.keys():
            temp_dict = dict()
            for classifier in self.classifiers:
                temp_dict[classifier] = 0
            self.__rates_count[k] = temp_dict

        for k, size_info_list in self.__rates.items():
            count = 0
            size_info_len = len(size_info_list)
            for size_info in size_info_list:
                count += 1
                print('{}: count_by_classifier: ({}/{})'.format(k, count, size_info_len))
                for classifier in self.classifiers:
                    if classifier.lower() in size_info.lower():
                        self.__rates_count[k][classifier] += 1
                        break

    def __pie_sub_plot(self, ax, data, title):
        """
        画某一品牌商品的各个分类的饼状图
        :param ax: plt.subplots 中返回的 ax
        :param data: 一个键为分类标准，值为数量的字典，如{'32G':1,'64G':2}
        :param title: 饼状图的标题
        """
        keys = list(data.keys())
        values = list(data.values())
        labels = keys
        sizes = values

        patches, l_text, p_text = ax.pie(sizes, labels=labels, labeldistance=1.1, autopct='%2.1f%%', shadow=False,
                                         startangle=90, pctdistance=0.6)
        for t in l_text:
            t.set_size = (30)
        for t in p_text:
            t.set_size = (20)
        ax.axis('equal')
        ax.legend()
        ax.set_title(title)

    def __save_pie_plot(self):
        """
        画所有品牌的饼状图

        :return: 一个 matplotlib.pyplot 实例
        """
        scale = 5
        fig, axes = plt.subplots(nrows=int(floor(sqrt(len(self.__rates_count)))),
                                 ncols=int(ceil(sqrt(len(self.__rates_count)))),
                                 figsize=(
                                     int(ceil(sqrt(len(self.__rates_count)))) * scale,
                                     int(floor(sqrt(len(self.__rates_count)))) * scale))
        count = 0
        for ax_row in axes:
            for ax in ax_row:
                key, value = list(self.__rates_count.items())[count]
                self.__pie_sub_plot(ax, value, key)
                count += 1
        return fig

    def run(self):
        """
        运行商品尺寸分析器，画出饼状图。

        :return: 一个 matplotlib.pyplot 实例
        """
        self.__read_rates_by_brand()
        self.__count_by_classifier()
        return self.__save_pie_plot()
