from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from music import settings
from user_player.views import player_view, SongView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('player/', player_view),
    path('song/', SongView.as_view()),
]

if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL)
