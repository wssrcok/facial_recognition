from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from website.forms import UploadFileForm, UploadMultipleFileForm
from website.models import Files
from django.views.generic.edit import FormView
from django.contrib import messages
import os

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


class UploadMultipleView(FormView):
    form_class = UploadMultipleFileForm
    template_name = 'upload_view.html'
    def get(self, request):
        # UploadTemplate = 'upload_view.html'
        # return render(request, UploadTemplate)
        form = UploadMultipleFileForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('images')
        if form.is_valid():
            for f in files:
                # print(f) -> xxx.jpg
                instance = Files(upload=f, uploader=request.POST.get('uploader'))
                instance.save()
                messages.success(request, 'Upload images successful')
            return render(request, self.template_name, {'form': form})
        else:
            return self.form_invalid(form)

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
