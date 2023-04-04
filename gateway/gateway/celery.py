import os

from celery import Celery

from gateway import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gateway.settings')

app = Celery('gateway', broker=settings.RABBITMQ_HOST)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
