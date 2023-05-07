from django.apps import AppConfig


class ArtistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'artist'

    def ready(self):
        from utils.consumers import UserCreatedListener, UserLoggedInListener
        threads = []
        user_created_listener = UserCreatedListener()
        user_logged_in_listener = UserLoggedInListener()
        threads.extend([user_created_listener, user_logged_in_listener])
        for thread in threads:
            thread.daemon = True
            thread.start()
