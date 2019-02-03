from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from website.forms import UploadFileForm
from website.models import Files
import os
# Create your views here.

def index(request):
    # files = Files.objects.all()
    # return render(request, 'index.html', {'files': files})
    staticDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images/')
    names= []
    for (dirpath, dirnames, filenames) in os.walk(staticDir):
        names.extend(filenames)
        break
    return render(request, 'index.html', {'fileNames': names})

class UploadView(TemplateView):
    UploadTemplate = 'upload_view.html'

    def get(self, request):
        # UploadTemplate = 'upload_view.html'
        # return render(request, UploadTemplate)
        form = UploadFileForm()

        return render(request, self.UploadTemplate, {'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        print("got")
        if form.is_valid():
            # file is saved
            # form.save()
            print("its here")
            instance = Files(upload=request.FILES['image'], uploader=request.POST.get('uploader'))
            instance.save()

            return HttpResponse("success")
        return render(request, self.UploadTemplate, {'form': form})

class SuccessView(TemplateView):
    UploadTemplate = 'success.html'

    def get(self, request):
        UploadTemplate = 'success.html'
        return render(request, UploadTemplate)

class AboutUsView(TemplateView):
    UploadTemplate = 'about_us.html'

    def get(self, request):
        UploadTemplate = 'about_us.html'
        return render(request, UploadTemplate)
