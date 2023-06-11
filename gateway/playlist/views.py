import logging

import grpc
from drf_yasg.utils import swagger_auto_schema
from google.protobuf.json_format import MessageToDict
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import common_pb2
import song_pb2_grpc
from gateway.settings import SERVICES
import playlist_pb2
import playlist_pb2_grpc
from playlist.serializers import PlaylistUpdateSerializer, PlaylistCreateSerializer


class PlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with grpc.insecure_channel(SERVICES['playlist']) as channel:
            stub = playlist_pb2_grpc.PlaylistServiceStub(channel)
            try:
                res = stub.GetAll(playlist_pb2.UserId(id=request.user.account.id))
                playlists = MessageToDict(res)['playlists']
                for playlist in playlists:
                    songs = playlist.get('songs')
                    if songs and len(songs) > 0:
                        full_songs = get_song_info(songs)
                        playlist['songs'] = full_songs
                    else:
                        playlist['songs'] = []
                return Response(data=playlists, status=status.HTTP_200_OK)
            except grpc.RpcError as e:
                logging.error(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logging.error(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=PlaylistCreateSerializer)
    def post(self, request):
        with grpc.insecure_channel(SERVICES['playlist']) as channel:
            stub = playlist_pb2_grpc.PlaylistServiceStub(channel)
            try:
                res = stub.Create(playlist_pb2.CreateRequest(name=request.data['name'], user=request.user.account.id))
                playlist = MessageToDict(res)
                return Response(data=playlist, status=status.HTTP_201_CREATED)
            except grpc.RpcError as e:
                logging.error(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logging.error(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        with grpc.insecure_channel(SERVICES['playlist']) as channel:
            stub = playlist_pb2_grpc.PlaylistServiceStub(channel)
            try:
                stub.Delete(playlist_pb2.SongId(id=request.data['id']))
                return Response(status=status.HTTP_204_NO_CONTENT)
            except grpc.RpcError as e:
                logging.error(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logging.error(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlaylistDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        with grpc.insecure_channel(SERVICES['playlist']) as channel:
            stub = playlist_pb2_grpc.PlaylistServiceStub(channel)
            try:
                res = stub.GetById(playlist_pb2.SongId(id=pk))
                playlist = MessageToDict(res)
                songs = playlist.get('songs')
                if songs and len(songs) > 0:
                    full_songs = get_song_info(songs)
                    playlist['songs'] = full_songs
                else:
                    playlist['songs'] = []
                return Response(data=playlist, status=status.HTTP_200_OK)
            except grpc.RpcError as e:
                logging.error(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logging.error(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=PlaylistUpdateSerializer)
    def put(self, request, pk):
        with grpc.insecure_channel(SERVICES['playlist']) as channel:
            stub = playlist_pb2_grpc.PlaylistServiceStub(channel)
            try:
                res = stub.AddSongsToPlaylist(playlist_pb2.AddRequest(playlist=pk, songs=request.data['songs']))
                playlist = MessageToDict(res)
                return Response(data=playlist, status=status.HTTP_200_OK)
            except grpc.RpcError as e:
                logging.error(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logging.error(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_song_info(songs: list):
    with grpc.insecure_channel(SERVICES['music']) as channel:
        stub = song_pb2_grpc.SongServiceStub(channel)
        try:
            res = stub.GetSongs(common_pb2.Ids(id=songs))
            songs = MessageToDict(res)
            return songs['songs']
        except grpc.RpcError as e:
            logging.error(e)
            return []
        except Exception as e:
            logging.error(e)
            return []
