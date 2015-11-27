# -*- coding: utf-8 -*-
import os

class Config(object):
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MINT_SERVICE_URL=os.environ.get('MINT_SERVICE_URL', 'http://country.openregister.dev:4567')
    READ_API_URL=os.environ.get('READ_API_URL', 'http://country.openregister.dev:8080')

class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'local-dev-not-secret')

class TestConfig(Config):
    TESTING = True
