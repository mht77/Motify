from django.contrib import admin

from song.models import Genre, Album, Song


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name'
    ]
    list_editable = [
        'name'
    ]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'date_added'
    ]
    list_editable = [
        'name'
    ]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'file',
        'genre',
        'album',
        'no_plays',
        'date_added',
        'path'
        # 'length'
    ]

