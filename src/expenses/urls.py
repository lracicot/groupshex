from django.conf.urls import patterns, url

from expenses import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)