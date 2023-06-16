import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from user_player.middlewares import AuthMiddleware
from user_player.urls import urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddleware(AllowedHostsOriginValidator(URLRouter(urlpatterns))),
    }
)