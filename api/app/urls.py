from django.conf.urls import patterns, include, url

from django.contrib.auth.views import login, logout

from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name = 'home'),
    url(r'^accounts/login/$', login, name = 'login'),
    url(r'^accounts/logout/$', logout, name = 'logout'),
    url(r'^done/$', views.done, name='done'),

    url(r'^login/$', views.mylogin, name = 'mylogin' ),
    url(r'^logout/$', views.mylogout, name= 'mylogout' ),

    # following features have not been checked yet
    url(r'^signup-email/', views.signup_email),
    url(r'^email-sent/', views.validation_sent),
    url(r'^email/$', views.require_email, name='require_email'),
)
