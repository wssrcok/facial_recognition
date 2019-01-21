from django.urls import path

from . import views
from website.views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('upload/success', SuccessView.as_view(), name='success')
]