from ast import literal_eval
from os import getenv

from dotenv import load_dotenv

from application.api.database import database_file

load_dotenv()


class Config(object):
    '''Parent configuration class.'''
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET = getenv('SECRET')

    SQLALCHEMY_DATABASE_URI = database_file
    SQLALCHEMY_TRACK_MODIFICATIONS = literal_eval(
        getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
    SQLALCHEMY_ECHO = literal_eval(getenv('SQLALCHEMY_ECHO'))
    JSON_SORT_KEYS = literal_eval(getenv('JSON_SORT_KEYS'))



class DevelopmentConfig(Config):
    '''Configurations for Development.'''
    DEBUG = True


class TestingConfig(Config):
    '''Configurations for Testing, with a separate test database.'''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True


class StagingConfig(Config):
    '''Configurations for Staging.'''
    DEBUG = True


class ProductionConfig(Config):
    '''Configurations for Production.'''
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
