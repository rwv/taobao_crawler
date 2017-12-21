#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json

from .model import Item
from .utils import *


class ItemCrawler:
    """
    爬取淘宝手机商品记录，插入到 mongodb 数据库中。
    插入数据示例：{
    "is_crawled" : true,
    "seller_id" : "360622108",
    "sellerLoc" : "广东 深圳",
    "location" : "广东 深圳",
    "title" : "4+64G指纹识别!全网通4G智能手机5.5寸大屏",
    "item_id" : "561319321061",
    "price" : "529.00",
    "area" : "深圳",
    "sold" : "0"
    }
    """

    def __init__(self, keywords, db, timeout=3):
        """
        初始化 ItemCrawler 实例

        :param keywords: 搜索的关键词 list，如 ['手机','Phone']
        :param db: 一个 pymongo.MongoClient.db 的实例
        :param timeout: 爬取超时时间, 默认值为 3
        """
        self.__db = db
        self.__collection = self.__db.items
        self.keywords = keywords
        self.timeout = timeout

    def run(self):
        """
        运行商品信息爬虫，插入至数据库中。
        """
        urls = []
        pages_count = 5000
        for i in range(1, pages_count + 1):
            for keyword in self.keywords:
                urls.append("http://s.m.taobao.com/search?q={}&m=api4h5&page=".format(keyword) + str(i))

        for url in urls:
            print(url)
            body = get_body(url, self.timeout)
            if len(body) == 0:
                continue
            else:
                if len(json.loads(body)['listItem']) == 0:
                    break
            items = self.__parse(body)
            self.__add_items(items)

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
            if self.__collection.find({'item_id': item.item_id}).count() == 0:
                self.__collection.insert(item.dict())
