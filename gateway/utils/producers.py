from abc import ABC

import msgpack
import pika

from gateway import settings


class Producer(ABC):
    """
    parent class for publishing msg on a rabbitmq queue
    """
    def __init__(self):
        self.channel = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        self.channel = self.connection.channel()


class SendNotification(Producer):
    """
    send notif msg on the certain queue
    """
    def call(self, msg):
        self.channel.basic_publish(exchange='notification', routing_key='in-app-notif', body=msgpack.packb(msg))
        self.channel.close()
        self.connection.close()


class UserCreatedEvent(Producer):
    """
    send user created msg on the fanout exchange
    """
    def call(self, account):
        self.channel.exchange_declare(exchange='user-created', exchange_type='fanout')
        self.channel.basic_publish(exchange='user-created', routing_key='', body=msgpack.packb(account))
        self.channel.close()
        self.connection.close()
