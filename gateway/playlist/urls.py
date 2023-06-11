from django.urls import path

from playlist.views import PlaylistView, PlaylistDetailView

urlpatterns = [
    path('playlists/', PlaylistView.as_view()),
    path('playlists/<str:pk>/', PlaylistDetailView.as_view()),
]
