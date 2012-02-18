from django.conf.urls.defaults import patterns, include, url
from example.exampleApp import views

urlpatterns = patterns('',
    url(r'^$', views.appIndex),
    url(r'^system/info/$', views.sysInfo)
    #url(r'^system/info/$', views.sysInfo)
    
) 
