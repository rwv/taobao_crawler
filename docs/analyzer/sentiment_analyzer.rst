Sentiment Analyzer
=======================

遍历 rates collection, 对当中每个评论进行情感分析，并将其存入 rates_sentiments collection 中。

用法
-------

生成分析器实例
~~~~~~~~~~~~~~~~~
::

    from taobao_crawler.analyzer.sentiment_analyzer import SentimentAnalyzer
    analyzer = SentimentAnalyzer(db)

``SentimentAnalyzer(db)`` 中的 ``db`` 参见 :doc:`../utils/db`

运行情感分析器
~~~~~~~~~~~~~~~~~~
::

    analyzer.run()

类属性
--------

.. autoclass:: analyzer.sentiment_analyzer.SentimentAnalyzer
    :members:
    :undoc-members:
    :show-inheritance: