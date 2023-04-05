import requests
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from account.serializers import AccountSerializer, UserOutputSerializer, UserInputSerializer, UserUpdateSerializer
from gateway import settings
from utils.cache_decorator import use_cache


# noinspection PyMethodMayBeStatic
class UserView(APIView):
    """
    Handles user get, registration (POST) and info update (PUT) requests
    """

    def get_permissions(self):
        # Allow GET and PUT requests only if user is authenticated
        if self.request.method in ['GET', 'PUT']:
            return [IsAuthenticated()]
        else:
            # Allow all other requests (e.g. POST) without authentication
            return [AllowAny()]

    @use_cache
    def get(self, request):
        """
        Return the details of the authenticated user
        """
        return Response(data=UserOutputSerializer(request.user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserInputSerializer)
    def post(self, request):
        """
        Register a new user
        """
        serializer = UserInputSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=UserOutputSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserUpdateSerializer)
    def put(self, request):
        """
        Update the details of the authenticated user
        """
        serializer = UserUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=request.user, validated_data=serializer.validated_data)
            return Response(data=UserOutputSerializer(request.user).data,
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountView(APIView):
    """
    handle user account info and the subscription update requests
    """

    def get_permissions(self):
        if self.request.method in ['GET', 'PUT']:
            return [IsAuthenticated()]

    @use_cache
    def get(self, request):
        """
        Return the account of the authenticated user
        """
        return Response(data=AccountSerializer(request.user.account).data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(request_body=AccountSerializer)
    # def put(self, request):
    #     """
    #     Update the account of the authenticated user
    #     """
    #     serializer = AccountSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.update(instance=request.user.account, validated_data=serializer.data)
    #         return Response(data=AccountSerializer(request.user.account).data, status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)


# noinspection PyBroadException
class GoogleAuthView(APIView):
    """
    handles google login api and create/login user
    """

    @swagger_auto_schema(operation_id='google_auth',
                         operation_description='login/signup google',
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['token'],
                             properties={
                                 'token': openapi.Schema(type=openapi.TYPE_STRING),
                             }))
    @action(methods=['post'], detail=True)
    def post(self, request):
        """token verification and get data from Google then login or create user"""
        try:
            tk = request.data['token']
            id_token.verify_oauth2_token(tk, google_requests.Request(), settings.CLIENT_ID)
            response = requests.get('https://oauth2.googleapis.com/tokeninfo?id_token=' + tk)
            data = response.json()
            if response.status_code != status.HTTP_200_OK:
                return Response(data=data, status=response.status_code)
            email = data['email']
            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                user = User.objects.create_user(username=email, email=email)
            return Response(data={'access': str(AccessToken.for_user(user))}, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response(data={'detail': 'validation failed!'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
