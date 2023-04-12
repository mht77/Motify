import song_pb2
import song_pb2_grpc
from song.models import Song


# noinspection PyUnusedLocal
class SearchService(song_pb2_grpc.SearchService):

    def Find(self, request, target, **kwargs):
        songs = [song_pb2.Song(id=song.id, name=song.name, artist=song.artist.name, genre=song.genre.name,
                               album=song.album.name, date_added=song.date_added.strftime("%Y-%m-%d %H:%M:%S"))
                 for song in Song.objects.filter(name__icontains=request.keyword)]
        songs.extend([song_pb2.Song(id=song.id, name=song.name, artist=song.artist.name, genre=song.genre.name,
                                    album=song.album.name, date_added=song.date_added.strftime("%Y-%m-%d %H:%M:%S"))
                      for song in Song.objects.filter(artist__name__icontains=request.keyword)])
        return song_pb2.SearchResponse(songs=songs)
