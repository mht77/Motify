from concurrent import futures

import grpc
from django.core.management.base import BaseCommand

from music import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server.add_insecure_port('[::]:' + settings.GRPC_PORT)
        server.start()
        print("Server started, listening on " + settings.GRPC_PORT)
        server.wait_for_termination()
