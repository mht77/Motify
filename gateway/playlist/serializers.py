from rest_framework import serializers


class PlaylistCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=True)
    songs = serializers.ListField(child=serializers.IntegerField(), required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PlaylistUpdateSerializer(serializers.Serializer):
    songs = serializers.ListField(child=serializers.IntegerField(), required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
