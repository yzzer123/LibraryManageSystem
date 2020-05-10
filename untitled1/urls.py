"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import os

from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from BuctLib import views
from django.views.generic.base import RedirectView
urlpatterns = (
    path('admin/', admin.site.urls),
    path('loginout/', views.loginout),
    path(r'', views.loginpage),
    path(r'debug/', views.hello),
    path(r'pwdmdf/', views.pwdmdf),
    path(r'login/', views.logincheck),
    path(r'register/', views.register),
    path(r'readerindex/', views.readerindex),
    path(r'registercheck/', views.registerCheck),
    path(r'404/', views.page404),
    path(r'jump/', views.jump),
    path(r'checkpwd/', views.checkpwd),
    path(r'applyclass/', views.apllyclass),
    url(r'infomdf/', views.infmdf, name="modify information"),
    url(r'favicon.ico/', RedirectView.as_view(url=r'/static/img/icons/lib.svg')),

)
