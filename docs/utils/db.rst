DB
=======

生成 `DB` 示例以供其他模块使用

用法
-------

生成数据库实例
~~~~~~~~~~~~~~~~~
::

    db_config = {'db_user': '',  # 数据库用户名
                 'db_pass': '',  # 数据库密码
                 'db_host': 'localhost',  # 数据库地址
                 'db_port': 27017,  # 数据库端口
                 'db_name': 'taobao'}  # 数据库 collection 名称
    mongo = DB(db_config)

与其他模块搭配使用
~~~~~~~~~~~~~~~~~~~~
::

    rate_crawler = RateCrawler(mongo.db)

关闭数据库连接
~~~~~~~~~~~~~~~~~~~~
::

    mongo.close()


类属性
---------

.. autoclass:: utils.db.DB
    :members:
    :undoc-members:
    :show-inheritance: