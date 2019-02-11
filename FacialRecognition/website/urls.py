from django.urls import path
from django.conf.urls import url

from . import views
from website.views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('upload/', UploadMultipleView.as_view(), name='upload'),
    path('download/', DownloadView.as_view(), name='download'),
    url('download/handler', download_handler),
]