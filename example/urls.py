from django.conf.urls.defaults import patterns, include, url
from example import views


urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^about/(?P<section>[-\w]+)/$', views.about),
    
    # Website app
    url(r'^exampleapp/', include('exampleApp.urls')),
)
