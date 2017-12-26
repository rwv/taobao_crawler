Comment Analyzer
==================

根据评论分析词频，保存词云。

用法
-------

得到词云

生成评论分析器实例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    brands = ['vivo', 'oppo', 'mi', 'huawei', 'apple', 'SMARTISAN']
    from taobao_crawler.analyzer.comment_analyzer import CommentAnalyzer
    comm_analyzer = CommentAnalyzer(db)
    comm_analyzer.set_brand(brands)

``CommentAnalyzer(db)`` 中的 ``db`` 参见 :doc:`../utils/db`

得到各品牌评论词汇频率比例
~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    comm_analyzer.frequency_run()

得到各品牌评论词汇超平均值比例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    comm_analyzer.times_run()

数据示例
------------
::

    [('顶多', 20.856220399929835),
     ('谁家', 20.856220399929835),
     ('真没想到', 20.856220399929835),
     ('炸裂', 20.856220399929835),
     ('比安卓好', 20.856220399929835),
     ('有所改善', 20.856220399929835),
     ('老师', 20.856220399929835),
     ('直板', 20.856220399929835),
     ('恭维', 20.856220399929835),
     ('亲亲', 20.856220399929835)]

类属性
--------

.. autoclass:: analyzer.comment_analyzer.CommentAnalyzer
    :members:
    :undoc-members:
    :show-inheritance:
