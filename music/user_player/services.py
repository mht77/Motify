import datetime

import jwt

import account_pb2
from account_pb2_grpc import UserPlayerAuthService
from music import settings
from user_player.models import Device


class PlayerAuthService(UserPlayerAuthService):
    def GetUserToken(self, request, context, *args, **kwargs):
        print(context.invocation_metadata()[1].value)  # TODO
        print(context.invocation_metadata()[2].value)
        ip = context.invocation_metadata()[1].value
        device = context.invocation_metadata()[2].value
        access_expired = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_ACCESS_EXPIRATION_DELTA)
        device_en, created = Device.objects.get_or_create(user=request.id, ip=ip)
        if created:
            device_en.success = True
            device_en.name = device
            device_en.user = request.id
            device_en.save()
        access_token = jwt.encode({'account_id': request.id, 'exp': access_expired, 'ip': ip, 'device': device,
                                   'device_id': device_en.id}, settings.SECRET_KEY, algorithm='HS256')
        return account_pb2.GetUserTokenResponse(token=access_token, device_id=str(device_en.id))
