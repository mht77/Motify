from django.contrib import admin

from artist.models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'NoPlays'
    ]
