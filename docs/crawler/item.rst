Item Crawler
=============

进行商品信息和评论的爬取

用法
-------

在项目中引入爬虫,示例

生成评论爬虫实例
~~~~~~~~~~~~~~~~~
::

    keywords = ['手机', 'Phone']
    from taobao_crawler.crawler.item import ItemCrawler
    crawler = ItemCrawler(keywords, db)

``ItemCrawler(keywords, db)`` 中的 ``db`` 参见 :doc:`../utils/db`

运行商品信息爬虫
~~~~~~~~~~~~~~~~~
::

    crawler.run()

数据示例
----------
::

    {
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

类属性
--------

.. autoclass:: crawler.item.ItemCrawler
    :members:
    :undoc-members:
    :show-inheritance: