from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import TemplateView
from website.forms import *
from website.models import UploadModel
from django.views.generic.edit import FormView
from django.contrib import messages
from FacialRecognition.settings import BASE_DIR
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
import os
import zipfile
from io import BytesIO
from threading import Thread
from .known_process import known_process_main
from .unknown_recognition import recognition_main

def index(request):
    # files = Files.objects.all()
    # return render(request, 'index.html', {'files': files})
    staticDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images/')
    names= []
    for (dirpath, dirnames, filenames) in os.walk(staticDir):
        names.extend(filenames)
        break
    return render(request, 'index.html', {'fileNames': names})

class UploadMultipleView(FormView):
    form_class = UploadMultipleFileForm
    template_name = 'upload_view.html'
    def get(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('upload')
        if form.is_valid():
            for f in files:
                # print(f) -> xxx.jpg
                instance = UploadModel(upload=f, uploader=request.POST.get('uploader'))
                instance.save()
                messages.success(request, 'Upload images successful')
            return render(request, self.template_name, {'form': form})
        else:
            return self.form_invalid(form)

class DownloadView(TemplateView):
    template_name = 'download_view.html'
    def get(self, request):
        return render(request, self.template_name)

    # def post(self, request, *args, **kwargs):
    #     model_object = UploadModel.objects.get(pk=1) #get an instance of model which has an ImageField
    #     context = {'image' : model_object.upload}
    #     html = render(request , 'download_view.html' , context)
    #     return response

# https://stackoverflow.com/questions/12881294/django-create-a-zip-of-multiple-files-and-make-it-downloadable
def download_handler(request):

    file_paths = [str(model_object.upload) for model_object in UploadModel.objects.all()]
    zip_subdir = "your_faces"
    zip_filename = "%s.zip" % zip_subdir
    # Open StringIO to grab in-memory ZIP contents
    s = BytesIO()
    # The zip compressor
    zf = zipfile.ZipFile(s, "w")
    for fpath in file_paths:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)
    zf.close()
    response = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # ..and correct content-disposition
    response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return response

class BackendView(FormView):
    form_class = UserInputForm
    template_name = 'backend_view.html'
    def get(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return render(request, self.template_name, {'form': form, 'fileNames':[]})
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if "process" in request.POST:
            thread = Thread(target = known_process_main)
            thread.start()
            messages.success(request, 'processing file')
            return render(request, self.template_name, {'form': UserInputForm(), 'fileNames':[]})
        elif "userinput" in request.POST:
            if form.is_valid():
                file_path = request.FILES['upload']
                filename = str(file_path).split()[-1] 
                instance = UploadModel(upload=file_path, uploader='userinput')
                instance.save()
                tolerance = 0.4 # will take userinput later
                retrived_file_paths = recognition_main(file_path, tolerance)
                if filename in retrived_file_paths:
                    retrived_file_paths.remove(filename)
                instance.delete()
                messages.success(request, 'retrive file successful' + str(retrived_file_paths))
                return render(request, self.template_name, {'form': form, 'fileNames': retrived_file_paths}) 



class AboutUsView(TemplateView):
    template_name = 'about_us.html'

    def get(self, request):
        template_name = 'about_us.html'
        return render(request, template_name)

# not using these funcitons right now

def download_single_image(request):
    model_object = UploadModel.objects.get(pk=2)
    file_path = str(model_object.upload)
    filename = str(model_object)
    with open(file_path, 'rb') as image:
        response = HttpResponse(image.read(), content_type='image/jpeg')
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Disposition'] = 'attachement; filename=%s' % filename
        return response

class UploadView(TemplateView):
    UploadTemplate = 'upload_view.html'

    def get(self, request):
        form = UploadForm()
        return render(request, self.UploadTemplate, {'form': form})

    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            # form.save()
            instance = UploadModel(upload=request.FILES['upload'], uploader=request.POST.get('uploader'))
            instance.save()

            return HttpResponse("success")
        return render(request, self.UploadTemplate, {'form': form})