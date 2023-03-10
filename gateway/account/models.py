import uuid

from django.contrib.auth.models import User
from django.core import serializers
from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from utils.producers import UserCreatedEvent


class Subscriptions(models.TextChoices):
    UNKNOWN = 'UNKNOWN', _('Unknown')
    BASIC = 'BASIC', _('Basic')
    STANDARD = 'STANDARD', _('Standard')
    PREMIUM = 'PREMIUM', _('Premium')


class Account(models.Model):
    id = models.CharField(max_length=40,
                          primary_key=True)

    user = models.OneToOneField(User,
                                on_delete=CASCADE,
                                related_name='account')

    subscription = models.CharField(max_length=8,
                                    choices=Subscriptions.choices,
                                    default=Subscriptions.BASIC)

    def __str__(self):
        return self.user.username + '_account'


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    """
    create account whenever a user model created
    :param sender: the model type
    :param instance: the instance of model
    :param created: if it is new (created on db) or it is updated
    """
    if instance and created and sender is User:
        account = Account(user=instance, id=uuid.uuid4())
        account.save()
        UserCreatedEvent().call(account=serializers.serialize("json", account))
