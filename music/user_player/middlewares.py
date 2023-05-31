import logging

import jwt
from channels.security.websocket import WebsocketDenier

from music import settings


class AuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # check if the user is authenticated by verifying the authorization header
        try:
            token = scope['query_string'].decode('utf-8')
            claims = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            scope['user'] = claims['account_id']
            scope['device'] = claims['device']
            scope['ip'] = claims['ip']
            return await self.app(scope, receive, send)
        except Exception as e:
            logging.error(e)
            denier = WebsocketDenier()
            return await denier(scope, receive, send)