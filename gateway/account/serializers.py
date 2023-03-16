import uuid

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from account.models import Account
from utils.producers import UserCreatedEvent


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


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    """
    create account whenever a user model created
    :param sender: the model type
    :param instance: the instance of model
    :param created: if it is new (created on db) or it is updated
    """
    if instance and created and sender is User:
        account = Account.objects.create(user=instance, id=uuid.uuid4())
        UserCreatedEvent().call(account=AccountSerializer(account).data)
