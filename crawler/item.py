#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
sys.path.append("../")
import requests
from utils.db import *
from utils.config import *
from utils.model import *

api_url = r'http://s.m.taobao.com/search'
params = {
    'q': '',
    'm': 'api4h5',
    'page': 1
}


class ItemCrawler:
    def __init__(self):
        """
        数据库初始化
        """
        self.client = init_client()
        self.db = self.client[db_config['db_name']]
        self.collection = self.db.items

    def run(self, keywords, pages_count):
        """
        爬取商品

        :param keywords: 产品关键字
        :param pages_count: 爬取页数
        :return: None
        """
        for i in range(1, pages_count + 1):
            params['page'] = i
            for keyword in keywords:
                params['q'] = keyword
                r = requests.get(url=api_url, params=params)
                print(r.url)
                data = r.json()['listItem']
                print(data)
                if not data:
                    continue
                else:
                    self.__add_items(data)
        self.__close()

    def __add_items(self, items):
        """
        将商品信息添加到数据库中

        :param items: list of item json
        :return: None
        """
        for item in items:
            data = Item(item, False)
            if self.collection.find({'item_id': Item.item_id}).count() == 0:
                self.collection.insert(item)

    def __close(self):
        """ 关闭数据库 """
        self.client.close()


if __name__ == '__main__':
    crawler = ItemCrawler()
    crawler.run(keywords=['手机'], pages_count=10)
