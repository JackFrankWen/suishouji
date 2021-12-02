# config.py
import os

class Config(object):
    """Base config, uses staging database server."""
    TESTING = False
    DB_SERVER = '192.168.1.56'

class ProductionConfig:
    """Uses production database server."""
    DB_SERVER = 'localhost'
    DB_NAME = "bookkeeppro"
    DB_USER = "root"
    DB_PASSWORD = "root"
    CLASSES = "bg-light"
    TITLE = "快速记"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{psw}@localhost/bookkeeppro".format(user="root", psw="root")


class DevelopmentConfig:
    DB_SERVER = 'localhost'
    TITLE = "测试模式"
    CLASSES = "bg-warning"
    DB_NAME = "bookkeepdev"
    DB_USER = "root"
    DB_PASSWORD = "root"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/bookkeepdev'



app_config = {
    'development': DevelopmentConfig(),
    'production': ProductionConfig()
}


def get_config():
    if os.environ.get('FLASK_ENV') == "development":

        config = app_config['development']
    else:
        config = app_config['production']
    return config

mysql_config = {
    'host': "localhost",
    'dbname': "bookkeep",
    'user': "root",
    'pwd': "root"
}

