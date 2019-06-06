import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
    instance.profile.save()
    
@receiver(post_delete, sender=User)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.profile.image:
        if os.path.isfile(instance.profile.image.path):
            os.remove(instance.profile.image.path)
        
@receiver(pre_save, sender=User)
def auto_delete_image_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    
    try:
        old_image = sender.objects.get(pk=instance.pk).profile.image
    except sender.DoesNotExist:
        return False
    
    new_image = instance.profile.image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)