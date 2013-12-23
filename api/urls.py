from django.conf.urls import patterns, include, url
from django.contrib import admin
from api import settings

from api.app import views

import api.apiv1.urls as api_urls
import api.app.urls as app_urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(api_urls)),
    url(r'^app/', include(app_urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^images/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)
