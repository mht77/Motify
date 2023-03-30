import uuid

from django.db import models

from song.models import Song


class Device(models.Model):
    name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    user = models.CharField(
        max_length=40,
        unique=True
    )

    ip = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user[:8] + self.name


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

    device = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user + '_player'
