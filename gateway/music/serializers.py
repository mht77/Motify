from rest_framework import serializers


class ArtistSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    user = serializers.CharField(max_length=40)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
