import os
import sys


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    FRONTEND_URL = '*'
    MEDIA_ROOT = '../media/'
    MEDIA_URL = '/media/'
    JSON_SORT_KEYS = False


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


config_class_name = os.getenv('APP_CONFIG_CLASS')
config = getattr(sys.modules[__name__], config_class_name)
