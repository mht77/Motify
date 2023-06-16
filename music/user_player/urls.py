from django.urls import path, re_path

from user_player.views import UserPlayerConsumer

urlpatterns = [
    re_path(r"^user_player", UserPlayerConsumer.as_asgi()),
]
