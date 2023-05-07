from django.contrib import admin

from user_player.models import Device, UserPlayer


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'ip',
        'name',
        'success'
    ]


@admin.register(UserPlayer)
class UserPlayerAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'current_song',
        'device',
        'second',
        'state'
    ]
