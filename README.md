# Taobao Crawler

[![Documentation Status](https://readthedocs.org/projects/taobao-crawler/badge/?version=latest)](http://taobao-crawler.readthedocs.io/)

## 技术细节
1. 爬取淘宝网上手机的商品信息（参数、销量、评分）和商品评论文本；
2. 将爬取到的信息存储进 Mongodb 中；
3. 处理评论文本数据
  * 使用 `jieba` 对数据进行词频分析，进行词云等数据可视化
  * 通过 `SnowNLP` 对数据进行NLP分析
    - 情感分析，与淘宝评分系统的结果相比较，将结果定为偏差程度，并考察偏差可能（水军，刷评）
4. 处理商品信息
  * 数据可视化
    - 各价位各品牌各款手机的占有率/好感度
    - 商品销售趋势
    - 配置占有率趋势
    - 各品牌产品线设置

## TODO

* [ ] Travis-CI & Coveralls
* [ ] unittest
* [ ] ShowNLP multiprocessing

