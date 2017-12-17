#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys

sys.path.append("../")
from utils.model import Item
from utils.utils import *

reload(sys)
sys.setdefaultencoding('utf8')


class ItemCrawler:
    """ 爬取淘宝手机商品记录 """

    def __init__(self, keywords):
        self.client, self.db = init_client()
        self.collection = self.db.items
        self.keywords = keywords

    def run(self):
        urls = []
        pages_count = 5000
        for i in range(1, pages_count + 1):
            for keyword in self.keywords:
                urls.append("http://s.m.taobao.com/search?q={}&m=api4h5&page=".format(keyword) + str(i))

        for url in urls:
            print url
            body = get_body(url)
            if len(body) == 0:
                continue
            else:
                if len(json.loads(body)['listItem']) == 0:
                    break
            items = self.__parse(body)
            self.__add_items(items)

        self.__close()

    def __parse(self, body):
        """ 解析商品记录 """
        items = []
        try:
            data = json.loads(body)
        except:
            return []
        item_list = data['listItem']
        if len(item_list) == 0:
            return []
        for _item in item_list:
            item = Item(_item['item_id'], _item['userId'], _item['title'], _item['area'], _item['location'],
                        _item['sellerLoc'], _item['price'], _item['sold'], False)
            items.append(item)
        return items

    def __add_items(self, items):
        """ 添加商品记录到数据库 """
        for item in items:
            if self.collection.find({'item_id': item.item_id}).count() == 0:
                self.collection.insert(item.dict())

    def __close(self):
        """ 关闭数据库 """
        self.client.close()
