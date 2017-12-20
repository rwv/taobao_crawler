import pymongo


class DB:
    def __init__(self, db_config):
        client = pymongo.MongoClient(db_config['db_host'], db_config['db_port'])
        if len(db_config['db_user']) != 0:
            admin = client[db_config['db_name']]
            admin.authenticate(db_config['db_user'], db_config['db_pass'])
        self.__client = client
        self.db = client[db_config['db_name']]

    def close(self):
        self.__client.close()
