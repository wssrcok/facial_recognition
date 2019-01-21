from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from website.forms import UploadFileForm
from website.models import Files


def index(request):
    return HttpResponse("Hello, world. You're at the index.")

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

            return HttpResponse("succes")
        return render(request, 'upload_view.html', {'form': form})

class SuccessView(TemplateView):
    UploadTemplate = 'success.html'

    def get(self, request):
        UploadTemplate = 'success.html'
        return render(request, UploadTemplate)