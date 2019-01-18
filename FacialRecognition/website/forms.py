from django import forms
from django.forms import ModelForm
from website.models import Files

class UploadFileFormOld(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class UploadFileForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
    class Meta:
        model = Files
        fields = ['uploader']
