import grpc
from google.protobuf.json_format import MessageToDict
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from gateway.settings import SERVICES

import artist_pb2
import artist_pb2_grpc


# noinspection PyMethodMayBeStatic
class ArtistView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, *args, **kwargs):
        with grpc.insecure_channel(SERVICES['music']) as channel:
            stub = artist_pb2_grpc.ArtistServiceStub(channel)
            try:
                if pk:
                    res = stub.GetArtist(artist_pb2.Id(id=pk))
                    return Response(data=MessageToDict(res), status=status.HTTP_200_OK)
                else:
                    res = stub.GetArtists(artist_pb2.Ids(id=[]))
                    return Response(data=MessageToDict(res)['artists'], status=status.HTTP_200_OK)
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                return Response(status=status.HTTP_400_BAD_REQUEST)
