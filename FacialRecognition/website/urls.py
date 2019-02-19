from django.urls import path
from django.conf.urls import url

from . import views
from website.views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('upload/', UploadMultipleView.as_view(), name='upload'),
    path('backend/', BackendView.as_view(), name='backend'),
    path('download/', DownloadView.as_view(), name='download'),
    url(r'^signup/$', views.signup_view, name="signup"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url('download/handler', download_handler),
]