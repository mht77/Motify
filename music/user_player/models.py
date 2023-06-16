import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from song.models import Song


class Device(models.Model):
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    user = models.CharField(
        max_length=40
    )

    ip = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    success = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'ip'), )

    def __str__(self):
        return self.ip + '_' + self.name


class PlayerState(models.TextChoices):
    PLAYING = 'PLAYING', _('Playing')
    PAUSED = 'PAUSED', _('Paused')


class UserPlayer(models.Model):
    id = models.CharField(
        max_length=40,
        primary_key=True,
        default=uuid.uuid4
    )

    user = models.CharField(
        max_length=40,
        unique=True
    )

    current_song = models.ForeignKey(
        Song,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    second = models.PositiveIntegerField(default=0)

    state = models.CharField(
        max_length=10,
        choices=PlayerState.choices,
        default=PlayerState.PAUSED
    )

    device = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user + '_player'
