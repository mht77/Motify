import uuid

from mutagen.mp3 import MP3

from django.db import models

from artist.models import Artist


class Genre(models.Model):
    id = models.CharField(
        max_length=40,
        primary_key=True,
        default=uuid.uuid4
    )

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Album(models.Model):
    id = models.CharField(
        max_length=40,
        primary_key=True,
        default=uuid.uuid4
    )

    name = models.CharField(max_length=30)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    id = models.CharField(
        max_length=40,
        primary_key=True,
        default=uuid.uuid4
    )

    file = models.FileField()

    name = models.CharField(max_length=30)

    artist = models.ForeignKey(
        Artist,
        related_name='songs',
        on_delete=models.CASCADE
    )

    album = models.ForeignKey(
        Album,
        related_name='songs',
        on_delete=models.CASCADE
    )

    genre = models.ForeignKey(
        Genre,
        related_name='songs',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    no_plays = models.PositiveBigIntegerField(default=0)

    date_added = models.DateTimeField(auto_now_add=True)

    # length = models.PositiveIntegerField()

    @property
    def path(self):
        return self.file.path

    def __str__(self):
        return f'{self.artist.name}-{self.name}'


# @pre_save