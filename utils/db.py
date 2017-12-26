import pymongo


class DB:
    def __init__(self, db_config):
        """
        初始化 utils.db.DB 实例

        :param db_config: 一个包含 'db_host', 'db_port', 'db_user', 'db_name', 'db_user', 'db_pass' 的字典
        """
        client = pymongo.MongoClient(db_config['db_host'], db_config['db_port'])
        if len(db_config['db_user']) != 0:
            admin = client[db_config['db_name']]
            admin.authenticate(db_config['db_user'], db_config['db_pass'])
        self.__client = client
        self.db = client[db_config['db_name']]

    def close(self):
        """
        关闭数据库连接
        """
        self.__client.close()
