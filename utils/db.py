import pymongo
from .config import db_config


def init_client():
    client = pymongo.MongoClient(db_config['db_host'], db_config['db_port'])
    if len(db_config['db_user']) != 0:
        admin = client[db_config['db_name']]
        admin.authenticate(db_config['db_user'], db_config['db_pass'])
    return client
