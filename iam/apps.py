from django.apps import AppConfig


class IamConfig(AppConfig):
    name = 'iam'

    def ready(self):
        import iam.signals