from django.apps import AppConfig

class UserRegistrationConfig(AppConfig):
    name = 'user_registration'

    def ready(self):
        import user_registration.signals
