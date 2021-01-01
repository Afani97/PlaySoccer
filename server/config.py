import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/play_soccer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    ORIGIN = ["http://localhost:8080", "http://127.0.0.1:5000"]


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=os.environ.get('PS_USER'),pw=os.environ.get('PS_PW'),url=os.environ.get('PS_URL'),db=os.environ.get('PS_DB'))
    ORIGIN = "https://playsoccer.dev"
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class AppiumTestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/play_soccer_test'


NON_NULL_STRING = {
    'type': 'string',
    'minLength': 1
}
