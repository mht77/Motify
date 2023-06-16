import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.core.cache import cache

from user_player.models import UserPlayer, PlayerState, Device
from user_player.serializers import UserPlayerSerializer


class UserPlayerConsumer(JsonWebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.scope['user'], self.channel_name
        )
        self.accept()
        print('connected: ', self.scope['user'], self.scope['device'])
        # self.send_json({'message': 'connected'})
        user_player = UserPlayer.objects.filter(user=self.scope['user']).first()
        cache.set(self.scope['user'], UserPlayerSerializer(user_player).data)
        self.send_json(UserPlayerSerializer(user_player).data)

    def disconnect(self, close_code):
        try:
            device = Device.objects.get(ip=self.scope['ip'], user=self.scope['user'])
            user_player = UserPlayer.objects.filter(user=self.scope['user']).first()
            if device.id == user_player.device.id:
                try:
                    ch = cache.get(self.scope['user'])
                    if ch:
                        user_player.second = ch['second']
                except KeyError:
                    pass
                user_player.state = PlayerState.PAUSED
                user_player.save()
                cache.delete(self.scope['user'])
        except Device.DoesNotExist:
            pass
        except UserPlayer.DoesNotExist:
            pass
        except Exception as e:
            logging.error(e)

    def receive_json(self, content, **kwargs):
        """
        Called with decoded JSON content.
        """
        cache_player = cache.get(self.scope['user'])
        second = cache_player.get('second', 0)
        if content.get('song') or content.get('device') or content.get('state'):
            user_player = UserPlayer.objects.filter(user=self.scope['user']).first()
            try:
                user_player.state = content.get('state', user_player.state)
                if content.get('song'):
                    user_player.current_song_id = content['song']
                    user_player.current_song.no_plays += 1
                    user_player.current_song.save()
                if content.get('device'):
                    user_player.device_id = content['device']
                user_player.save()
                cache_player = UserPlayerSerializer(user_player).data
                cache_player['second'] = second
            except KeyError:
                pass
        if content.get('second'):
            cache_player['second'] = content['second']
        cache.set(self.scope['user'], cache_player)
        async_to_sync(self.channel_layer.group_send)(
            self.scope['user'], {'type': 'user_player_update', 'message': cache_player}
        )
        # self.send_json(UserPlayerSerializer(user_player).data)

    def user_player_update(self, event):
        self.send_json(event['message'])
