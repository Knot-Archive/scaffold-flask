import os

from dotenv import find_dotenv
from dotenv import load_dotenv

from common.libs.Singleton import SingletonType


class BaseConfig:
    # SERVER_NAME = 'localhost:8001'
    FLASK_RUN_PORT = '8001'
    SECRET_KEY = "CZJ23KP9HKyujjurjhRRX4DoW6pQD2MxFK"
    DEBUG = True
    """flask-sqlalchemy"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """mail"""
    # MAIL_SERVER :# 默认为 ‘localhost’
    # MAIL_PORT : # 默认为 25
    # MAIL_USE_TLS : # 默认为 False
    # MAIL_USE_SSL : # 默认为 False
    # MAIL_DEBUG : # 默认为 app.debug
    # MAIL_USERNAME : #  默认为 None
    # MAIL_PASSWORD : # 默认为 None
    # MAIL_DEFAULT_SENDER : # 默认为 None
    # MAIL_MAX_EMAILS : # 默认为 None
    # MAIL_SUPPRESS_SEND : # 默认为 app.testing
    # MAIL_ASCII_ATTACHMENTS : # 默认为 False


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    pass


class DockerComposeConfig(BaseConfig):
    pass


class ConfigInstanceFactory:

    def get_config_instance(self):
        config_key = self.app_conf()
        if config_key == 'prod':
            return ProductionConfig
        elif config_key == 'dev':
            return DevelopmentConfig
        elif config_key == 'docker':
            return DockerComposeConfig
        elif config_key == 'default':
            return DevelopmentConfig

    def app_conf(self):
        load_dotenv(find_dotenv())
        config_key = os.environ.get('FLASK_CONF')
        assert config_key in ['prod', 'dev', 'docker', 'default']
        return config_key
