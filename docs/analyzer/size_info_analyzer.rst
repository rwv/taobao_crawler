Size Info Analyzer
=======================

商品尺寸分析器，由关键词，分类器生成饼状图。

用法
-------

生成分析器实例
~~~~~~~~~~~~~~~~~
::

    keywords = {'小米': ['米', 'mi'], '苹果': ['苹果', 'apple', 'iphone']}
    classifiers = ['16G', '32G', '64G', '128G', '256G']
    from taobao_crawler.analyzer.size_info_analyzer import SizeInfoAnalyzer
    analyzer = SizeInfoAnalyzer(keywords, classifiers, db)

``SizeInfoAnalyzer(keywords, classifiers, db)`` 中的 ``db`` 参见 :doc:`../utils/db`

生成饼状图
~~~~~~~~~~~~~~~~~~
::

    analyzer.run()

类属性
--------

.. autoclass:: analyzer.size_info_analyzer.SizeInfoAnalyzer
    :members:
    :undoc-members:
    :show-inheritance: