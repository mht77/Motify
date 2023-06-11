from django.test import TestCase

import song_pb2
from artist.models import Artist
from song.models import Song, Genre, Album
from song.services import SongService


class SearchServiceTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(name='test', user='test')
        self.genre = Genre.objects.create(name='test')
        self.album = Album.objects.create(name='test')

    def test_search(self):
        # arrange
        _ = Song.objects.create(name='test',
                                artist=self.artist,
                                genre=self.genre,
                                album=self.album,
                                file='test.mp3'
                                )
        # act
        res = SongService().Find(song_pb2.SearchRequest(keyword='te'), None)
        # assert
        self.assertEqual(len(res.songs), 2)
