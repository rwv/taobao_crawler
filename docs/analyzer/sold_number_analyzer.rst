Sold Number Analyzer
=======================

商品销量分析器，由关键词，分类器生成堆栈图。

用法
-------

生成分析器实例
~~~~~~~~~~~~~~~~~
::

    keywords = {'小米': ['米', 'mi'], '苹果': ['苹果', 'apple', 'iphone']}
    from taobao_crawler.analyzer.sold_number_analyzer import SoldNumberAnalyzer
    analyzer = SoldNumberAnalyzer(keywords, db)

``SoldNumberAnalyzer(keywords, db)`` 中的 ``db`` 参见 :doc:`../utils/db`

生成饼状图
~~~~~~~~~~~~~~~~~~
::

    analyzer.run()

类属性
--------

.. autoclass:: analyzer.sold_number_analyzer.SoldNumberAnalyzer
    :members:
    :undoc-members:
    :show-inheritance: