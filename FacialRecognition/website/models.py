from django.db import models
from django import forms
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import os

# Create your models here.

class Files(models.Model):
    # file will be uploaded to MEDIA_ROOT/uploads
    # upload = models.FileField(upload_to='uploads/')
    upload = models.FileField(upload_to='website/static/images')
    uploader = models.CharField(max_length=100)

class UploadModel(models.Model):
    upload = models.ImageField(upload_to='website/static/images')
    uploader = models.CharField(max_length=100)

    def __str__(self):
        return str(self.upload).split('/')[-1]
    
# These two auto-delete files from filesystem when they are unneeded:

@receiver(models.signals.post_delete, sender=UploadModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `UploadModel` object is deleted.
    """
    if instance.upload:
        if os.path.isfile(instance.upload.path):
            os.remove(instance.upload.path)

@receiver(models.signals.pre_save, sender=UploadModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `UploadModel` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = UploadModel.objects.get(pk=instance.pk).upload
    except UploadModel.DoesNotExist:
        return False

    new_file = instance.upload
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

# every time you make a new model, don't forget it migrate it to the database
# $ python manage.py makemigrations
# $ python manage.py migrate