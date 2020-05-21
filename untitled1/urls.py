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
    path(r'admin_pwdmdf/', views.admin_pwdmdf),
    path(r'login/', views.logincheck),
    path(r'register/', views.register),
    path(r'readerindex/', views.readerindex),
    path(r'adminindex/', views.adminindex),
    path(r'registercheck/', views.registerCheck),
    path(r'book_operation/', views.book_admin),
    path(r'add_book/', views.add_book),
    path(r'404/', views.page404),
    path(r'jump/', views.jump),
    path(r'add_user/', views.add_user),
    path(r'add_class/', views.add_class),
    path(r'add_fine/', views.add_fine),
    path(r'resetApply/', views.resetapply),
    path(r'checkpwd/', views.checkpwd),
    path(r'admin_checkpwd/', views.admin_checkpwd),
    path(r'todaycommend/', views.commend),
    path(r'admin_todaylib/', views.admin_datavisual),
    path(r'todaylib/', views.datavisual),
    path(r'getmessage/', views.getmessage),
    path(r'applyclass/', views.apllyclass),
    path(r'getborrow/', views.getborrow),
    path(r'getmesnum/', views.getmesnum),
    path(r'notreturn/', views.showbred),
    path(r'return/', views.returnbook),
    path(r'cancelNotice/', views.cancelNotice),
    path(r'admin_infmdf/', views.admin_infmdf),
    path(r'returned/', views.showreturned),
    path(r'illegal/', views.showillegal),
    path(r'sendMessage/', views.sendMessage),
    path(r'sendNotice/', views.sendNotice),
    path(r'deletebr/', views.deletebr),
    path(r'admin_searchresult/', views.admin_searchbooks),
    url(r'checking/', views.checkingbooks, name='checking'),
    url(r'brrow/', views.borrow, name='borrow'),
    url(r'searchresult/', views.searchbooks, name="searchbooks"),
    url(r'delayreturn/(\d+)/$', views.delayreturn, name='delay'),
    url(r'illegalreport/(\d+)/$', views.illegal_report, name="illegal"),
    url(r'admin_allnotices', views.admin_allnotice, name='admin_allnotices'),
    url(r'admin_noticedetail/(\d+)/$', views.admin_noticedetail, name="admin_noticepage"),
    url(r'admin_bookdetail/(\d+)/$', views.admin_bookdetail, name='admin_bookdetail'),
    url(r'allnotice/', views.allnotice, name='allnotice'),
    url(r'noticedetail/(\d+)/$', views.noticedetail, name='noticepage'),
    url(r'bookdetail/(\d+)/$', views.bookdetail, name='bookdetail'),
    url(r'infomdf/', views.infmdf, name="modify information"),
    url(r'favicon.ico/', RedirectView.as_view(url=r'/static/img/icons/lib.svg')),
)
