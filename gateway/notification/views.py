import grpc
from google.protobuf.json_format import MessageToDict
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import notification_pb2
import notification_pb2_grpc
from gateway.settings import SERVICES


class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with grpc.insecure_channel(SERVICES['notification']) as channel:
            stub = notification_pb2_grpc.NotificationServiceStub(channel)
            try:
                res = stub.GetNotifications(notification_pb2.NotificationRequest(id=request.user.account.id))
                notifications = []
                for r in res:
                    notifications.append(MessageToDict(r))
                return Response(data=notifications, status=status.HTTP_200_OK)
            except grpc.RpcError as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
