from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from account.models import Account


class UserOutputSerializer(serializers.ModelSerializer):
    """
    User DTO for GET request
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'date_joined']


class UserInputSerializer(serializers.ModelSerializer):
    """
    User model DTO for POST request
    """
    password = serializers.CharField(required=True, min_length=8)

    email = serializers.EmailField(required=True, min_length=5,
                                   validators=[UniqueValidator(User.objects.all(), message="User already registered")])

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        fields = ['email', 'password']
        model = User


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    User model DTO for PUT request
    """
    password = serializers.CharField(required=True, min_length=8)
    email = serializers.EmailField(required=True, min_length=5)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['email', 'password']


class AccountSerializer(serializers.ModelSerializer):
    user = UserOutputSerializer()

    class Meta:
        model = Account
        fields = '__all__'
