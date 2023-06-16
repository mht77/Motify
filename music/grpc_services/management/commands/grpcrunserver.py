from concurrent import futures

import grpc
from django.core.management.base import BaseCommand

import account_pb2_grpc
import artist_pb2_grpc
import song_pb2_grpc
from artist.services import ArtistService
from music import settings
from song.services import SongService
from user_player.services import PlayerAuthService


class Command(BaseCommand):
    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        artist_pb2_grpc.add_ArtistServiceServicer_to_server(ArtistService(), server)
        song_pb2_grpc.add_SongServiceServicer_to_server(SongService(), server)
        account_pb2_grpc.add_UserPlayerAuthServiceServicer_to_server(PlayerAuthService(), server)
        server.add_insecure_port(f'{settings.GRPC_ADDRESS}:' + settings.GRPC_PORT)
        server.start()
        print("Server started, listening on " + settings.GRPC_PORT)
        server.wait_for_termination()
