from django.db import models


class Artist(models.Model):
    id = models.CharField(
        max_length=40,
        primary_key=True
    )

    name = models.CharField(
        max_length=20,
    )

    user = models.CharField(
        max_length=40,
        null=True,
        blank=True
    )

    NoPlays = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name
