from django.urls import path

from music.views import ArtistView

urlpatterns = [
    path('artists/', ArtistView.as_view()),
    path('artists/<str:pk>/', ArtistView.as_view()),
]
