# config.py

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

mysql_config = {
    'host': "127.0.0.1",
    'dbname': "bookkeep",
    'user': "root",
    'pwd': "root"
}

