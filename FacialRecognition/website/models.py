from django.db import models
from django import forms

# Create your models here.

class Files(models.Model):
    # file will be uploaded to MEDIA_ROOT/uploads
    # upload = models.FileField(upload_to='uploads/')
    upload = models.FileField(upload_to='website/static/images')
    uploader = models.CharField(max_length=100)

# this model maybe wrong
class Files_shenruochen(models.Model): 
    upload = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    uploader = models.CharField(max_length=100)

# every time you make a new model, don't forget it migrate it to the database
# $ python manage.py makemigrations
# $ python manage.py migrate