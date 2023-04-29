from django.urls import path
from . import views

app_name = 'parser'

urlpatterns = [
    path('pdf', views.ParsePDFView.as_view(), name='pdf')
]
