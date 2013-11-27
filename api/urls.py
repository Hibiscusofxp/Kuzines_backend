from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.auth.views import login, logout
# from api.app.views import mylogin, mylogout

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'api.app.views.home', name = 'home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup-email/', 'api.app.views.signup_email'),
    url(r'^email-sent/', 'api.app.views.validation_sent'),
    url(r'^login/$', 'api.app.views.home'),
    url(r'^done/$', 'api.app.views.done', name='done'),
    url(r'^email/$', 'api.app.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),

    # url(r'^logout/$', 'api.app.views.logout', name='logout'),
    url(r'^accounts/logout/$', logout, name = 'logout'),
    url(r'^accounts/login/$', login, name = 'login'),
    # url(r'^mylogin/$', mylogin, name = 'login'),
    # url(r'^mylogout/$', mylogout, name='logout'),
)
