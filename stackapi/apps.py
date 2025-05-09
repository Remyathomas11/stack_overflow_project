from django.apps import AppConfig


class StackapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stackapi'

    def ready(self):
        import stackapi.signals
