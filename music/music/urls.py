from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from music import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_player.urls')),
]

if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL)
