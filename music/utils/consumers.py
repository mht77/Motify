import abc
import logging
import threading

import msgpack as msgpack
import pika as pika

from music import settings
from user_player.models import Device, UserPlayer


class RabbitListener(threading.Thread, abc.ABC):
    """
    establish connection with rabbitmq
    listen on the specific exchange
    """

    def __init__(self, queue, exchange='', exchange_type='direct'):
        super().__init__()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST, heartbeat=5))
        self.channel = self.connection.channel()
        self.queue = queue
        self.exchange = exchange
        self.exchange_type = exchange_type

    def run(self):
        self.channel.queue_declare(queue=self.queue, durable=True)
        if self.exchange != '':
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True)
            self.channel.queue_bind(exchange=self.exchange, queue=self.queue)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    @abc.abstractmethod
    def callback(self, ch, method, properties, body):
        pass


class UserCreatedListener(RabbitListener):

    def __init__(self):
        super().__init__(queue='music_user', exchange='user-created', exchange_type='fanout')

    # noinspection PyUnusedLocal
    def callback(self, ch, method, properties, body):
        try:
            user_data = msgpack.unpackb(body)
            logging.info(f'User Created: {user_data}')
            UserPlayer.objects.create(user=user_data['id'])
        except Exception as e:
            print(e)


class UserLoggedInListener(RabbitListener):

    def __init__(self):
        super().__init__(queue='user_logged_in')

    # noinspection PyUnusedLocal
    def callback(self, ch, method, properties, body):
        try:
            device = msgpack.unpackb(body)
            logging.info(f'User logged in: {device}')
            entity, _ = Device.objects.filter(user=device['user']).get_or_create(ip=device['ip'])
            entity.name = device['device']
            entity.success = not device['failed']
            entity.user = device['user']
            entity.save()
            user_player = UserPlayer.objects.filter(user=device['user']).first()
            if user_player and not user_player.device:
                user_player.device = entity
                user_player.save()
        except Exception as e:
            logging.error(e)


class UserDeleteListener(RabbitListener):

    def __init__(self):
        super().__init__(queue='music_user_delete', exchange='user-delete', exchange_type='fanout')

    def callback(self, ch, method, properties, body):
        try:
            user_data = msgpack.unpackb(body)
            logging.info(f'User Deleted: {user_data}')
            UserPlayer.objects.filter(user=user_data['id']).delete()
            for device in Device.objects.filter(user=user_data['id']):
                device.delete()
        except Exception as e:
            logging.error(e)
