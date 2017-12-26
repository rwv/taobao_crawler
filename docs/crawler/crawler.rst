Crawler
=======

进行商品信息和评论的爬取

用法
-------

在项目中引入爬虫,示例::

    keywords = ['手机', 'Phone']
    from taobao_crawler.crawler import Crawler
    crawler = Crawler(keywords, db)

``Crawler(keywords, db)`` 中的 ``db`` 参见 :doc:`../utils/db`

运行商品信息爬虫
~~~~~~~~~~~~~~~~~
::

    crawler.item.run()

运行商品评论爬虫
~~~~~~~~~~~~~~~~~~
::

    crawler.rate.run()

运行商品信息及评论爬虫
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    crawler.run()



存入 mongodb 的数据范例参见 :doc:`./item`, :doc:`./rate`

类属性
---------

.. autoclass:: crawler.Crawler
    :members:
    :undoc-members:
    :show-inheritance: