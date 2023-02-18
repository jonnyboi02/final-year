"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
#from django.contrib import admin
from django.urls import path, include
from . import views
from .views import register, upload_NFT, create_account, get_accounts, send_transaction

app_name = 'app'


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', register),
    path('upload/', upload_NFT),
    path('create_account/', create_account),
    path('get_accounts/', get_accounts),
    path('send_transaction/', send_transaction)
    
]