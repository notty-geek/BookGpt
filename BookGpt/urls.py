"""
URL configuration for BookGpt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from services.chatbot.views import ChatHandlerView, ChatPromptView
from services.pdfparser.views import ParsePDFView
from services.swagger import spec

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('v1/parser/pdf', ParsePDFView.as_view(), name='parse_pdf'),
    path('v1/chat/', ChatHandlerView.as_view(), name='get_response'),
    path('v1/prompts/', ChatPromptView.as_view(), name='chat_prompt_list'),
    path('v1/swagger-ui', spec.generate_yaml_to_ui, name='swagger_ui'),

]
