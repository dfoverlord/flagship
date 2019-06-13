from django.contrib import admin

from .models import Image, PhotoBook

# Support adminsortable2 optionally
import importlib
from django.utils.safestring import mark_safe
if importlib.util.find_spec('adminsortable2', 'admin'):
    from adminsortable2.admin import SortableAdminMixin
else:
    # Mock up class for mixin
    class SortableAdminMixin:
        mock = True

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'thumbnail_image', 'date_taken', 'date_upload')
    list_filter = ('image_photobooks',)
    list_per_page = 25
    readonly_fields = ('thumbnail_image',)
    
    def thumbnail_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url = obj.data_thumbnail.url,
            width = obj.data_thumbnail.width,
            height = obj.data_thumbnail.height,
            )
    )
        
        
class PhotoBookAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'title')
    list_display_links = ('title',)
    if hasattr(SortableAdminMixin, 'mock'):
        list_editable = ('order',)
        list_display = ('title', 'order')
    filter_horizontal = ('images',)
    raw_id_fields = ('highlight',)
    
    
admin.site.register(Image, ImageAdmin)
admin.site.register(PhotoBook, PhotoBookAdmin)