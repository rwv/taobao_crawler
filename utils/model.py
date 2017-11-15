# -*- coding:utf-8 -*-

class Item:
    def __init__(self, info, is_crawled):
        self.item_id = info['item_id']
        self.info = info
        self.is_crawled = is_crawled

    def dict(self):
        return {
            'item_id': self.item_id,
            'item_info': self.info,
            'is_crawled': self.is_crawled
        }

class FailedUrl:
    def __init__(self, url):
        self.url = url

    def dict(self):
        return {'url': self.url}

