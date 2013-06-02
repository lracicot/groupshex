from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('expenses.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/', include('login.urls')),
    url(r'^accounts/', include('social_auth.urls')),
)
