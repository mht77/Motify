from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _


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
