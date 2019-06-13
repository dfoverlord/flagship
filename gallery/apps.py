from django.apps import AppConfig


class GalleryConfig(AppConfig):
    name = 'gallery'
    verbose_name = 'Digital Facets Gallery'
    
    def ready(self):
        import gallery.signals