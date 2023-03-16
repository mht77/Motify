import threading

import msgpack as msgpack
import pika as pika

from music import settings


class UserCreatedListener(threading.Thread):
    """
    establish connection with rabbitmq
    listen on the specific exchange
    """

    def __init__(self):
        super().__init__()
        self.retry = 0
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST, heartbeat=5))
        self.channel = self.connection.channel()

    # noinspection PyUnusedLocal
    # @staticmethod
    def callback(self, ch, method, properties, body):
        try:
            print(f'User Created: {msgpack.unpackb(body)["id"]}')
            print(f'User Created: {msgpack.unpackb(body)}')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.retry = 0
        except Exception as e:
            print(e)
            self.retry += 1
            if self.retry > 5:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                self.retry = 0
            else:
                ch.basic_nack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.queue_declare(queue='music_user', durable=True)
        self.channel.exchange_declare(exchange='user-created', exchange_type='fanout')
        self.channel.queue_bind(exchange='user-created', queue='music_user')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='music_user', on_message_callback=self.callback)
        self.channel.start_consuming()
