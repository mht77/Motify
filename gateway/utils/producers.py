from abc import ABC, abstractmethod

import msgpack
import pika

from gateway import settings


class Producer(ABC):
    """
    parent class for publishing msg on a rabbitmq queue
    """

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        self.channel = self.connection.channel()

    @abstractmethod
    def call(self, data):
        pass


class SendNotification(Producer):
    """
    send notif msg on the certain queue
    """

    def call(self, msg):
        self.channel.basic_publish(exchange='notification', routing_key='notif', body=msgpack.packb(msg))
        self.channel.close()
        self.connection.close()


class UserCreatedEvent(Producer):
    """
    send user created msg on the fanout exchange
    """

    def call(self, account):
        self.channel.exchange_declare(exchange='user-created', exchange_type='fanout', durable=True)
        self.channel.basic_publish(exchange='user-created', routing_key='', body=msgpack.packb(account))
        self.channel.close()
        self.connection.close()


class UserLoggedIn(Producer):
    """
    send user logged msg on the direct exchange
    """

    def call(self, device):
        self.channel.basic_publish(exchange='', routing_key='user_logged_in', body=msgpack.packb(device))
        self.channel.close()
        self.connection.close()


class UserDelete(Producer):
    """
    send user delete msg on the fanout exchange
    """

    def call(self, account):
        self.channel.exchange_declare(exchange='user-delete', exchange_type='fanout', durable=True)
        self.channel.basic_publish(exchange='user-delete', routing_key='', body=msgpack.packb(account))
        self.channel.close()
        self.connection.close()
