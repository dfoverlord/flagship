import os
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.functional import cached_property
from PIL import Image as pImage
from io import BytesIO
from PIL.ExifTags import TAGS
from pathlib import Path
from datetime import datetime
from django.core.files.base import ContentFile

# Create your models here.
class Image(models.Model):
    data = models.ImageField(upload_to='images')
    data_thumbnail = models.ImageField(upload_to='thumbs', editable=False)
    date_upload = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=60, blank=True)
    
    @cached_property
    def slug(self):
        return slugify(self.title)
        
    @cached_property
    def exif(self):
        exif_data = {}
        self.data.open()
        with pImage.open(self.data) as img:
            if hasattr(img, '_getexif'):
                info = img._getexif()
                if not info:
                    return {}
                
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    exif_data[decoded] = value
                    
                if 'FNumber' in exif_data:
                    exif_data['Aperture'] = str(exif_data['FNumber'][0] / exif_data['FNumber'][1])
                    
                if 'ExposureTime' in exif_data:
                    exif_data['Exposure'] = "{0}/{1}".format(exif_data['ExposureTime'][0], exif_data['ExposureTime'][1])
        return exif_data
        
    @cached_property
    def date_taken(self):
        original_exif = self.exif.get('DateTimeOriginal')
        if not original_exif:
            return self.mtime
        
        try:
            return datetime.strptime(original_exif, "%Y:%m:%d %H:%M:%S")
        except ValueError:  
            """ Fall back to file modification time """
            return self.mtime
            
    @cached_property
    def mtime(self):
        return datetime.fromtimestamp(os.path.getmtime(self.data.path))
        
    @property
    def title(self):
        if hasattr(self, '_title'):
            return self._title
        """ Derive a title from the original filename """
        
        """ remove extension """
        filename = Path(self.data.name).with_suffix('').name
        
        """ convert spacing characters to whitespaces """
        name = filename.translate(str.maketrans('_', ' '))
        
        """ return with first letter caps """
        return name.title()
        
    """
    Temporary override for photobook highlights
    """
    @title.setter
    def title(self, name):
        self._title = name
         
    def get_absolute_url(self):
        return reverse('gallery:image_detail', kwargs={'pk': self.pk, 'slug': self.slug})
        
    def __str__(self):
        return self.title
         
    def save(self, *args, **kwargs):
        if not self.data.closed:
            if not self.make_thumbnail():
                raise Exception('Could not create thumbnail - is the file type valid?')
                
        super(Image, self).save(*args, **kwargs)
        
        img = pImage.open(self.data.path)
        if img.height > 1000 or img.width > 1000:
            output_size = (1000, 1000)
            img.thumbnail(output_size)
            img.save(self.data.path)
        
    def make_thumbnail(self):
        img = pImage.open(self.data)
        output_size = (350, 350)
        img.thumbnail(output_size, pImage.ANTIALIAS)
        
        thumb_name, thumb_extension = os.path.splitext(self.data.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + '_thumb' + thumb_extension
        
        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            """ unrecognized file type """
            return False
            
        """
        Save thumbnail to in-memory file as StringIO
        """
        temp_thumb = BytesIO()
        img.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)
        
        """
        set save=FALSE, otherwise it will run in an infinite loop
        """
        self.data_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
        
        return True
    
    
class PhotoBook(models.Model):
    title = models.CharField(max_length=250)
    images = models.ManyToManyField(Image, blank=True, related_name='image_photobooks')
    highlight = models.OneToOneField(Image, related_name='photobook_highlight', null=True, blank=True, on_delete=models.SET_NULL)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    
    class Meta(object):
        ordering = ['order', '-pk']
        
    @property
    def slug(self):
        return slugify(self.title)
        
    @property
    def display_highlight(self):
        """ if there is no highlight but there are images in the album, use the first """
        if not self.highlight and self.images.count():
            img = self.images.earliest('id')
        else:
            img = self.highlight
        
        if img:
            """
            use the photobook title instead of the highlight title
            """
            img.title = self.title
            
        return img
    
    def get_absolute_url(self):
        return reverse('gallery:photobook_detail', kwargs={'pk': self.pk, 'slug': self.slug})
    
    def __str__(self):
        return self.title
