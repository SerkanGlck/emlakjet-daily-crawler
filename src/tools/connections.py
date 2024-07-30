import pika
import redis
from src.tools.config import ConnectionsConfig


def connect_rabbitmq():
    credentials = pika.PlainCredentials(
        ConnectionsConfig.RABBITMQ_USER, ConnectionsConfig.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(ConnectionsConfig.RABBITMQ_HOST, ConnectionsConfig.RABBITMQ_PORT,
                                           ConnectionsConfig.RABBITMQ_VHOST, credentials, heartbeat=600,
                                           blocked_connection_timeout=500
                                           )

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    return channel


def connect_redis():
    return redis.Redis(
        host=ConnectionsConfig.REDIS_HOST, 
        port=ConnectionsConfig.REDIS_PORT, 
        db=0, 
        password=ConnectionsConfig.REDIS_PASSWORD,
        decode_responses=True
    )
