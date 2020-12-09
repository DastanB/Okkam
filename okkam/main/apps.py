from django.apps import AppConfig

class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        try:
            import okkam.main.signals
        except ImportError:
            pass
