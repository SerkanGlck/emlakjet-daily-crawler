import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

load_dotenv(os.path.join(basedir, '.env.a'))


class Config:
    APP_NAME = os.getenv('APP_NAME')
    DOMAIN = os.getenv('DOMAIN')
    QUEUE_NAME = os.getenv('QUEUE_NAME')
    RESULT_QUEUE_NAME = os.getenv('RESULT_QUEUE_NAME')
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    DEBUG = True if os.getenv('DEBUG') == "true" else False
    SLEEP_LONG = float(os.getenv('SLEEP_LONG'))
    SLEEP_SHORT = float(os.getenv('SLEEP_SHORT'))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT'))
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')


class ConnectionsConfig:
    RABBITMQ_USER = os.getenv('RABBITMQ_USER')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
    RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT'))
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST')

    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = int(os.getenv('REDIS_PORT'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
