from django.apps import AppConfig


class IamConfig(AppConfig):
    name = 'iam'
    verbose_name='Digital Facets Identity and Access Management'

    def ready(self):
        import iam.signals