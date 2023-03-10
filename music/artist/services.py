import uuid

import grpc

import artist_pb2
import artist_pb2_grpc
from artist.models import Artist


class ArtistService(artist_pb2_grpc.ArtistService):

    def GetArtist(self, request, target, **kwargs):
        try:
            artist = Artist.objects.get(id=request.id)
            return artist_pb2.Artist(id=artist.id, name=artist.name, no_plays=artist.NoPlays, user=artist.user)
        except Artist.DoesNotExist:
            target.set_code(grpc.StatusCode.NOT_FOUND)
            target.set_details("Artist not found")
            return artist_pb2.Artist()

    def CreateArtist(self, request, target, **kwargs):
        artist = Artist(id=uuid.uuid4(), name=request.name, user=request.user)
        artist.save()
        artist.refresh_from_db()
        return artist_pb2.Artist(id=artist.id, name=artist.name, no_plays=artist.NoPlays, user=artist.user)

    def GetArtists(self, request, target, **kwargs):
        artists = Artist.objects.filter(id__in=request.id)
        return artist_pb2.Artists(
            artists=[artist_pb2.Artist(id=artist.id, name=artist.name, no_plays=artist.NoPlays, user=artist.user)
                     for artist in artists])
