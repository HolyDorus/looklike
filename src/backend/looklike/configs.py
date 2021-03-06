import os
import sys


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    AVAILABLE_HOSTS = '*'
    JSON_SORT_KEYS = False
    MEDIA_URL = os.getenv('MEDIA_URL')


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


config_class_name = os.getenv('APP_CONFIG_CLASS')
config = getattr(sys.modules[__name__], config_class_name)
