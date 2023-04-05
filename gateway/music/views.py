import grpc
from drf_yasg.utils import swagger_auto_schema
from google.protobuf.json_format import MessageToDict
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Account
from account.serializers import AccountSerializer
from gateway.settings import SERVICES

import artist_pb2
import artist_pb2_grpc
from music.serializers import ArtistSerializer


class ArtistsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        with grpc.insecure_channel(SERVICES['music']) as channel:
            stub = artist_pb2_grpc.ArtistServiceStub(channel)
            try:
                res = stub.GetArtists(artist_pb2.Ids(id=[]))
                artists = MessageToDict(res)['artists']
                for artist in artists:
                    artist['account'] = AccountSerializer(Account.objects.get(id=artist['user'])).data
                return Response(data=artists, status=status.HTTP_200_OK)
            except grpc.RpcError as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=ArtistSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ArtistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        artist = artist_pb2.Artist(name=request.data['name'], user=request.data['user'])
        with grpc.insecure_channel(SERVICES['music']) as channel:
            stub = artist_pb2_grpc.ArtistServiceStub(channel)
            try:
                res = stub.CreateArtist(artist)
                artist = MessageToDict(res)
                artist['account'] = AccountSerializer(Account.objects.get(id=artist['user'])).data
                return Response(data=artist, status=status.HTTP_201_CREATED)
            except grpc.RpcError as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ArtistView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, *args, **kwargs):
        if not pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        with grpc.insecure_channel(SERVICES['music']) as channel:
            stub = artist_pb2_grpc.ArtistServiceStub(channel)
            try:
                res = stub.GetArtist(artist_pb2.Id(id=pk))
                artist = MessageToDict(res)
                artist['account'] = AccountSerializer(Account.objects.get(id=artist['user'])).data
                return Response(data=artist, status=status.HTTP_200_OK)
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
