Getting Started
=====================

安装依赖
--------
::

    $ pip install -r requirements.txt

爬取数据
--------
::

    from gevent import monkey
    monkey.patch_all() # gevent monkey patch all
    from taobao_crawler.utils.db import DB
    from taobao_crawler.crawler import Crawler

    db_config = {'db_user': '',  # 数据库用户名
                 'db_pass': '',  # 数据库密码
                 'db_host': 'localhost',  # 数据库地址
                 'db_port': 27017,  # 数据库端口
                 'db_name': 'taobao'}  # 数据库 collection 名称
    keywords = ['手机', 'Phone']

    mongo = DB(db_config)
    crawler = Crawler(keywords, mongo.db)
    crawler.run()

