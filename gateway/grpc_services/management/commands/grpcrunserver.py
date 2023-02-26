from concurrent import futures

import grpc
from django.core.management.base import BaseCommand

from grpc_services import user_pb2_grpc
from grpc_services.user_service import UserService


class Command(BaseCommand):
    def handle(self, *args, **options):
        port = '50051'
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
        server.add_insecure_port('[::]:' + port)
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()
