# -*- coding: utf-8 -*-
import os

class Config(object):
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MINT_SERVICE_URL=os.environ.get('MINT_SERVICE_URL', 'http://country.openregister.dev:4567')
    MINT_API_PASSWORD=os.environ.get('MINT_API_PASSWORD', 'some_password')
    READ_API_URL=os.environ.get('READ_API_URL', 'http://country.openregister.dev:8080')

    BASIC_AUTH_USERNAME=os.environ.get('BASIC_AUTH_USERNAME', 'openregister')
    BASIC_AUTH_PASSWORD=os.environ.get('BASIC_AUTH_PASSWORD', 'OpenRegister')
    BASIC_AUTH_REALM=os.environ.get('BASIC_AUTH_REALM', 'openregister')

class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'local-dev-not-secret')

class TestConfig(Config):
    TESTING = True
