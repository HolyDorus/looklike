import os
import sys

from dotenv import load_dotenv


# Load all values from .env file
load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    POSTGRESQL_URL = os.getenv('POSTGRESQL_URL')

    AVAILABLE_HOSTS = '*'
    JSON_SORT_KEYS = False
    MEDIA_URL = os.getenv('MEDIA_URL')


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


config_class_name = os.getenv('APP_CONFIG_CLASS')
config = getattr(sys.modules[__name__], config_class_name)
