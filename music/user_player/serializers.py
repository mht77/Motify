from rest_framework import serializers

from song.models import Song
from user_player.models import UserPlayer, Device


class SongSerializer(serializers.ModelSerializer):
    album = serializers.StringRelatedField()
    artist = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()

    class Meta:
        model = Song
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class UserPlayerSerializer(serializers.ModelSerializer):
    current_song = SongSerializer()

    device = DeviceSerializer()

    class Meta:
        model = UserPlayer
        fields = '__all__'
