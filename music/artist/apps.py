from django.apps import AppConfig


class ArtistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'artist'

    def ready(self):
        from utils.consumers import UserCreatedListener
        threads = []
        user_listener = UserCreatedListener()
        threads.append(user_listener)
        for thread in threads:
            thread.daemon = True
            thread.start()
