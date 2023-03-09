from concurrent import futures

import grpc
from django.core.management.base import BaseCommand

import account_pb2_grpc
from gateway import settings
from grpc_services.account_service import AccountService


class Command(BaseCommand):
    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        account_pb2_grpc.add_AccountServiceServicer_to_server(AccountService(), server)
        server.add_insecure_port('[::]:' + settings.GRPC_PORT)
        server.start()
        print("Server started, listening on " + settings.GRPC_PORT)
        server.wait_for_termination()
