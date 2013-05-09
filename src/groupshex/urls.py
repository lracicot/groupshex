from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

admin.autodiscover()
admin.site.unregister(Site)
admin.site.unregister(Group)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
