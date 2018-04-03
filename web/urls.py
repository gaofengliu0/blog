# -*- coding: UTF-8 -*-

from django.conf.urls import url
from .views import home,account

urlpatterns = [
    url(r'^login.html$', account.login),
    url(r'^logout.html$', account.logout),
    url(r'^register.html$', account.register),
    url(r'^check_code.html$', account.check_code),
    url(r'^$', home.index),
    url(r'^all/(?P<article_type_id>\d+).html',home.index,name='index'),
    url(r'^test/$',home.test,name='test'),

]