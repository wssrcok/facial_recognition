from django.urls import path
from django.conf.urls import url

from . import views
from website.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('upload/', UploadMultipleView.as_view(), name='upload'),
    path('backend/', BackendView.as_view(), name='backend'),
    path('download/', DownloadView.as_view(), name='download'),
    url('download/handler', download_handler),
]