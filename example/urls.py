from django.conf.urls.defaults import patterns, include, url
from example import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index),
    url(r'^about/(?P<section>[-\w]+)/$', views.about)
)
