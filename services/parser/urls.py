from django.urls import path
from . import views

app_name = 'pdfparser'

urlpatterns = [
    path('pdf', views.ParsePDFView.as_view()),
]
