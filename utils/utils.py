# -*- coding:utf-8 -*-
import pymongo
import requests
import requesocks
from model import FailedUrl
from config import *


# 初始化mongodb客户端
def init_client():
    client = pymongo.MongoClient(config['db_host'], config['db_port'])
    if len(config['db_user']) != 0:
        admin = client[config['db_name']]
        admin.authenticate(config['db_user'], config['db_pass'])
    return client


# 发送get请求
def get_body(url):
    retry_times = 0
    client = requests.session()
    while retry_times < 3:
        try:
            content = client.get(url, timeout=config['timeout']).content
            return content
        except:
            retry_times += 1
    return ''


# 把失败的url添加到数据库
def add_failed_url(db, url):
    collection = db.failed_urls
    if collection.find({'url': url}).count() == 0:
        collection.insert(FailedUrl(url).dict())

