Final Score Analyzer
======================

得到评论的标准评分。

用法
-------

根据评论分数分布得到商品最终标准评分

生成评论评分器实例
~~~~~~~~~~~~~~~~~~~~~~
::

    brands = ['vivo', 'oppo', 'mi', 'huawei', 'apple', 'SMARTISAN']
    from taobao_crawler.analyzer.final_score_analyzer import FinalScoreAnalyzer
    score_analyzer = FinalScoreAnalyzer(db)
    score_analyzer.set_brand(brands)

``FinalScoreAnalyzer(db)`` 中的 ``db`` 参见 :doc:`../utils/db`

查询某一商品分数分布
~~~~~~~~~~~~~~~~~~~~~~~
::

    item_id = ''
    score_analyzer.score_distribution_run(item_id)

查询某一商品标准分数
~~~~~~~~~~~~~~~~~~~~~
::

    item_id = ''
    score_analyzer.score_distribution_run(item_id)

保存三种评分两两散点图
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    score_analyzer.compared_score_run()

保存各品牌最终评分图
---------------------
::

        final_scores = self.three_score_to_final_score(self.three_scores, [0.43, 0.25, 0.32])
        self.draw_final_score(final_scores)

类属性
--------

.. autoclass:: analyzer.final_score_analyzer.FinalScoreAnalyzer
    :members:
    :undoc-members:
    :show-inheritance:
