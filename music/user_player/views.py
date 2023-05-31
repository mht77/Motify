from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from user_player.models import UserPlayer, PlayerState
from user_player.serializers import UserPlayerSerializer


class UserPlayerConsumer(JsonWebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.scope['user'], self.channel_name
        )
        self.accept()
        print('connected: ', self.scope['user'], self.scope['device'])
        self.send_json({'message': 'connected'})
        user_player = UserPlayer.objects.filter(user=self.scope['user']).first()
        self.send_json(UserPlayerSerializer(user_player).data)

    def disconnect(self, close_code):
        user_player = UserPlayer.objects.filter(user=self.scope['user']).first()
        user_player.state = PlayerState.PAUSED  # needs some changes TODO
        user_player.save()

    def receive_json(self, content, **kwargs):
        """
        Called with decoded JSON content.
        """
        user_player = UserPlayer.objects.filter(user=self.scope['user']).first()
        try:
            user_player.state = content.get('state', user_player.state)
            if content.get('song'):
                user_player.current_song_id = content['song']
            if content.get('device'):
                user_player.device_id = content['device']
            user_player.save()
        except KeyError:
            pass
        async_to_sync(self.channel_layer.group_send)(
            self.scope['user'], {'type': 'user_player_update', 'message': UserPlayerSerializer(user_player).data}
        )
        # self.send_json(UserPlayerSerializer(user_player).data)

    def user_player_update(self, event):
        self.send_json(event['message'])


