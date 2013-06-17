from django.conf.urls import patterns, url

from expenses import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^expenses/add$', views.add_expense, name='add_expense')
)