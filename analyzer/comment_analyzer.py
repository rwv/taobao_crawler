from collections import Counter

import jieba
from scipy.misc import imread
from wordcloud import WordCloud


class CommentAnalyzer:
    """
    利用NLP分析评论，词频得到词云
    """

    def __init__(self, db, brand_name=('vivo', 'oppo', 'mi', 'huawei', 'apple', 'SMARTISAN')):
        """
        :param db: 一个 pymongo.MongoClient.db 的实例
        :param brand_name: 所研究的所有品牌名
        """
        self.db = db
        self.rates = self.db.rates
        self.items = self.db.items
        self.brand_name = brand_name

    def set_brand(self, brand_name):
        """
        更改品牌名称

        :param brand_name: list, 品牌名称
        """
        self.brand_name = brand_name

    def brand_to_id(self, brand):
        """
        通过品牌名得到其下商品

        :param brand: list, 所研究的所有品牌名
        :return: iteration, 遍历该品牌下所有商品(dictionary)的iteration
        """
        return self.items.find({'title': {'$regex': ".{0}.*".format(brand)}})

    def id_to_comment(self, item_id):
        """
        通过商品ID得到其评论情感评分

        :param item_id: string, 商品ID
        :return: string, 该ID商品所有评论
        """
        comment = ''
        for comm in self.rates.find({'item_id': item_id}):
            comment += comm['rate_comment']
        return comment

    def draw_freq_wordcloud(self, string, color_mask_address, write_file_address):
        """
        保存词云

        :param string: string, 用以生成词云的字符串
        :param color_mask_address: 背景图片地址
        :param write_file_address: 图片保存地址
        """
        cut_text = " ".join(jieba.cut(string))
        color_mask = imread(color_mask_address)
        cloud = WordCloud(
            width=4000,
            height=2000,
            font_path="tk.ttf",  # Chinese-font
            background_color='white',
            mask=color_mask,
            max_words=2000,
            max_font_size=200
        )
        word_cloud = cloud.generate(cut_text)
        word_cloud.to_file(write_file_address)

    def get_counter(self, string):
        """
        生成计数器(Counter)，表示该字符串中各词汇的频次

        :param string: dictionary {词汇:该词汇频率与平均频率比例}
        :return: Counter{词汇:该词汇频率与平均频率比例}
        """
        li = [j for j in jieba.cut(string)]
        c = Counter(li)
        return c

    def get_ratio(self, c):
        """
        生成频率(Counter)，得到该词汇的出现频率

        :param c: Counter 计数器(Counter)，表示该字符串中各词汇的频次
        :return: dictionary{词汇:该词汇频率与平均频率比例}
        """
        s = sum(c.values())
        r = {key: value / s for key, value in c.items()}
        return r

    def get_times(self, r0, r, hold):
        """
        生成频率(Counter)，得到该词汇的出现频率

        :param r0: dictionary 表示该字符串中各词汇的频率
        :param r: dictionary 表示所有评论中各词汇的频次
        :param hold: float 阈值, 当比例超过该值时输出
        :return: dictionary{词汇:该词汇频率与平均频率比例}
        """
        times = {}
        for key, value in r0.items():
            if value / r[key] > hold:
                times[key] = value / r[key]
        return times

    def get_most(self, times, k):
        """
        得到倍数词典中最高倍数的前k个词汇

        :param times: dictionary {词汇，该词汇频率与平均频率比例}
        :param k: 选取词汇频率最高倍数中前k个
        :return: list, [(词汇，比例)]
        """
        return sorted(times.items(), key=lambda x: x[1])[:k]

    def draw_more_wordcloud(self, most, color_mask_address, write_file_address):
        """
        绘制超越平均词频倍数的词云

        :param most: dictionary {词汇，该词汇频率与平均频率比例}
        :param color_mask_address: 背景图片地址
        :param write_file_address: 图片保存地址
        """
        string = ''
        for word, time in most:
            string = string + ((word + ' ') * int(time)) + ' '
        self.draw_freq_wordcloud(string, color_mask_address, write_file_address)

    def run(self):
        """
        运行函数
        得到各品牌评论词云
        """
        comments = []
        coun = []
        ratio = []
        c_all = Counter()
        # freqWordCloud
        for i in range(len(self.brand_name)):
            for item in self.brand_to_id(self.brand_name[i]):
                item_id = item['item_id']
                comment = self.id_to_comment(item_id)
                comments.append(comment)
                li = [j for j in jieba.cut(comment)]
                coun.append(Counter(li))
                c_all += coun[i]
                ratio.append(self.get_ratio(coun[i]))
                self.draw_freq_wordcloud(comment, "{}.jpg".format(i), "freqWordCloud{}.png".format(i))

        # moreWordCloud
        times = []
        ltimes = []
        r_all = self.get_ratio(c_all)

        for i in range(len(self.brand_name)):
            times.append(self.get_times(ratio[i], r_all, 1))
            ltimes.append(self.get_most(times[i], 400))
            self.draw_more_wordcloud(ltimes[i], "{}.jpg".format(i), "moreWordCloud{}.png".format(i))
