from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'test'),
    url(r'^gmap/$', views.getListFromGoogleMap, name = 'gmap'),
)
