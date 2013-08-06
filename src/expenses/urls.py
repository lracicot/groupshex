from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from expenses import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^expenses/add$', views.add_expense, name='add_expense'),
    url(r'^expenses/get/(\d+)$', views.get_expenses, name='get_expense'),
    url(r'^expenses/(\d+)$', views.grouboard, name='grouboard'),
    url(r'^groups/$', views.manage_groups, name='manage_groups'),
    url(r'^groups/get/$', views.get_groups, name='get_groups'),
    url(r'^groups/fb-groups-list.html$', TemplateView.as_view(template_name='fb-groups-list.html'))
)
