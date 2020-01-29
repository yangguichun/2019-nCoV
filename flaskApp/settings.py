import os

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', '123456')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:00@127.0.0.1/feiyan'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    pass

class ProductConfig(BaseConfig):
    pass

config = {
    'development': DevelopmentConfig,
    'production': ProductConfig
}