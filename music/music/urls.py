from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from music import settings
from user_player.views import test_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('player/', test_view),
]
if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL)
