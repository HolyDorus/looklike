from os import getenv


class BaseConfig:
    SECRET_KEY = getenv('SECRET_KEY')
    JSON_SORT_KEYS = False


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False
