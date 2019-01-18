from django.db import models

# Create your models here.

class Files(models.Model):
    # file will be uploaded to MEDIA_ROOT/uploads
    upload = models.FileField(upload_to='uploads/')
    uploader = models.CharField(max_length=100)