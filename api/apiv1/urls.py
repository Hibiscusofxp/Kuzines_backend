from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^gmap$', views.getListFromGoogleMap, name = 'gmap'),
    url(r'^signup$', views.sign_up, name = 'signup'),
    url(r'^login$', views.log_in, name = 'login'),
    url(r'^islogin$', views.is_login, name = 'is_login'),
    url(r'^logout$', views.log_out, name = 'log_out'),
    url(r'^newpost$', views.newpost, name = 'newpost'),
    url(r'^getposts$', views.getPosts, name = 'getposts'),
    url(r'^getprofile$', views.getProfile, name = 'getprofile'),
    url(r'^uploadfile$', views.uploadFile, name = 'uploadfile'),
    url(r'^getreviews$', views.getReviews, name = 'getreviews'),
    url(r'^newrestaurant$', views.newRestaurant, name = 'newrestaurant'),
)
