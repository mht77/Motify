from django.urls import path

from music.views import ArtistsView, ArtistView

urlpatterns = [
    path('artists/', ArtistsView.as_view()),
    path('artists/<str:pk>/', ArtistView.as_view()),
]
