from django.contrib.auth.models import User
from django.db import models
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=60, blank=True)
    website = models.CharField(max_length=100, blank=True)
    short_bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(default='no_photo.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        super().save()
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
            
        """ Find code to delete legacy pics after user changes profile pic """