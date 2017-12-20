#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

from .model import FailedUrl


# 发送get请求
def get_body(url, timeout):
    retry_times = 0
    while retry_times < 3:
        try:
            content = requests.get(url, timeout=timeout).text
            return content
        except:
            retry_times += 1
    return ''


# 把失败的url添加到数据库
def add_failed_url(db, url):
    collection = db.failed_urls
    if collection.find({'url': url}).count() == 0:
        collection.insert(FailedUrl(url).dict())
