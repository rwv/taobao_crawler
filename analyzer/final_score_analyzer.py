import matplotlib.pyplot as plt
import numpy as np


class FinalScoreAnalyzer:
    """
    利用商品的评论信息，通过三种中间评分，得到一种对于商品的好评评分
    """

    def __init__(self, db, brand_name=('vivo', 'oppo', 'mi', 'huawei', 'apple', 'SMARTISAN')):
        """
        :param db: 一个 pymongo.MongoClient.db 的实例
        :param brand_name: 所研究的所有品牌名
        """
        self.db = db
        self.rates = self.db.rates
        self.items = self.db.items
        self.sentiments = self.db.rates_sentiments
        self.brand_name = list(brand_name)

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

    def id_to_each_score(self, item_id):
        """
        通过商品ID得到其评论情感评分

        :param item_id: string, 商品ID
        :return: list, 该ID商品所有评论的情感评分
        """
        score = [t['score'] for t in self.sentiments.find({'item_id': item_id})]
        return score

    def draw_scatter(self, x, y, title, write_file_address):
        """
        画散点图

        :param x: 横轴
        :param y: 纵轴
        :param title: 图片标题
        :param write_file_address: 图片保存地址
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_title(title)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.scatter(x, y, s=100, alpha=0.5)
        plt.legend(self.brand_name)
        plt.savefig(write_file_address)

    def draw_final_score(self, final_score):
        """
        画散点图

        :param final_score: list(shape=(m,n), m为品牌数,n为评论数)
        """
        color = ['r', 'b', 'g', 'y', 'm', 'c']
        length = len(self.brand_name)
        for i in range(length):
            y = final_score[i]
            x = np.random.random(y.shape[0])
            x = (x + i) * 1 / length
            plt.scatter(x, y, c=color[i], s=100, alpha=0.5)
        avg = [t.mean() for t in final_score]
        for i in range(length):
            left = i / length
            right = (i + 1) / length
            plt.plot([left, right], [avg[i], avg[i]], c=color[i], linewidth=2)
        plt.legend(self.brand_name)
        plt.savefig('Final Score.png')

    def score_to_three_score(self, score, fractile_parameter, good_comment_parameter):
        """
        根据一种评分得到三个评分

        :param score: 原始评分分数
        :param fractile_parameter: 分位数参数, (0,1)
        :param good_comment_parameter: 好评比例参数, (0,1)
        :return: list(平均数-分位数-好评比例)
        """
        if not score:
            return
        a = np.array(score)
        m0 = np.mean(a)
        m1 = sorted(a)[int(len(a) * fractile_parameter)]
        m2 = (a > good_comment_parameter).sum() / len(score)
        return [m0, m1, m2]

    def three_score_to_final_score(self, scores, weight):
        """
        根据三种评分得到最终评分

        :param scores: 三种评分
        :param weight: 三种评分权重
        :return: list(最终评分)
        """
        final_scores = []
        for score in scores:
            s0, s1, s2 = score[0], score[1], score[2]
            w0, w1, w2 = weight[0], weight[1], weight[2]
            final_scores.append(s0 * w0 + s1 * w1 + s2 * w2)
        return final_scores

    def run(self):
        """
        运行函数
        保存三种评分两两散点图与各品牌最终评分图
        """
        length = len(self.brand_name)
        three_scores = []
        for i in range(length):
            brand = self.brand_name[i]
            for item in self.brand_to_id(brand):
                item_id = item['item_id']
                score = self.id_to_each_score(item_id)
                three_score = self.score_to_three_score(score, 0.11, 0.53)
                if not three_score:
                    continue
                three_scores.append(three_score)

        # draw
        for i in range(length):
            ts = three_scores[i]
            brand = self.brand_name[i]
            self.draw_scatter(ts[0], ts[1], brand + '-mean-fractile', brand + '-mean-fractile.jpg')
            self.draw_scatter(ts[0], ts[1], brand + '-mean-good%', brand + '-mean-good%.jpg')

        # final score
        final_scores = self.three_score_to_final_score(three_scores, [0.43, 0.25, 0.32])
        self.draw_final_score(final_scores)
