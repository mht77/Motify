from concurrent import futures

import grpc
from django.core.management.base import BaseCommand

import artist_pb2_grpc
from artist.services import ArtistService
from music import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        artist_pb2_grpc.add_ArtistServiceServicer_to_server(ArtistService(), server)
        server.add_insecure_port('[::]:' + settings.GRPC_PORT)
        server.start()
        print("Server started, listening on " + settings.GRPC_PORT)
        server.wait_for_termination()