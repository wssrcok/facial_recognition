from django import forms
from django.forms import ModelForm
from website.models import Files, UploadModel

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['upload', 'uploader']

class UploadMultipleFileForm(forms.Form):
    uploader = forms.CharField(max_length=50)
    upload = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class UserInputForm(forms.Form):
    upload = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False})) 