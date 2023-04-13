from abc import ABC

import msgpack
import pika

from music import settings


class Producer(ABC):
    """
    parent class for publishing msg on a rabbitmq queue
    """

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        self.channel = self.connection.channel()


class SendNotification(Producer):
    """
    send notif msg on the certain queue
    """

    def call(self, msg):
        self.channel.basic_publish(exchange='notification', routing_key='notif', body=msgpack.packb(msg))
        self.channel.close()
        self.connection.close()
