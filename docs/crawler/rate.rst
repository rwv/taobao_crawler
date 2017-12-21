RateCrawler
=============

对数据库中未爬取评论的商品进行商品评论的爬取

用法
-------

在项目中引入爬虫,示例

生成评论爬虫实例
~~~~~~~~~~~~~~~~~
::

    from taobao_crawler.crawler.rate import RateCrawler
    rate_crawler = RateCrawler(keywords,db)

运行评论爬虫
~~~~~~~~~~~~~~~~~
::

    rate_crawler.run()

数据示例
----------
::

    {
        "_id" : ObjectId("5a1d600db0d7ee38b9b0c942"),
        "buyCount" : 0,
        "useful" : true,
        "item_id" : "560697135358",
        "rate_id" : NumberLong("331495062062"),
        "rateDate" : "2017-11-23 23:16:40",
        "rate_content" : "挺棒的手机 快递也快非常满意",
        "auctionSku" : "机身颜色:香槟色;套餐类型:官方标配;存储容量:64GB;版本类型:中国大陆",
        "anony" : true,
        "size_info" : "机身颜色:香槟色;套餐类型:官方标配;存储容量:64GB;版本类型:中国大陆"
    }

类属性
-----------

.. autoclass:: crawler.rate.RateCrawler
    :members:
    :undoc-members:
    :show-inheritance: