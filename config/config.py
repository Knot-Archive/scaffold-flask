import os

from flask.cli import load_dotenv

# ! this should before ConfigClass. Because class static variable __new__ cant get env.
load_dotenv()


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', "! need secret key")
    SERVER_NAME = os.environ.get('SERVER_NAME', 'localhost:8080')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = True

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
    """flask-sqlalchemy"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """flask-sqlalchemy"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    DEBUG = True


class DockerComposeConfig(BaseConfig):
    """flask-sqlalchemy"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    DEBUG = False


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
        config_key = os.environ.get('FLASK_CONF')
        assert config_key in ['prod', 'dev', 'docker', 'default']
        return config_key
