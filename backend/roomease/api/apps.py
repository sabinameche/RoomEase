from django.apps import AppConfig


class RoomConfig(AppConfig):
    name = 'api'

    def ready(self):
        import api.signals
