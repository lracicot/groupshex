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
    url(r'^groups/get/(\d+)$', views.get_group, name='get_group'),
    url(r'^groups/add_member/(\d+)/(\d+)$', views.add_member, name='add_member'),
    url(r'^groups/remove_member/(\d+)/(\d+)$', views.remove_member, name='remove_member'),
    url(r'^groups/get_members/(\d+)$', views.get_members, name='get_members'),
    url(r'^groups/get_not_members/(\d+)$', views.get_not_members, name='get_not_members'),
    url(r'^groups/add$', views.add_group, name='add_group'),
    url(r'^groups/members-list.html$', TemplateView.as_view(template_name='members-list.html')),
    url(r'^groups/groups-list.html$', TemplateView.as_view(template_name='groups-list.html')),
    url(r'^groups/groups-detail.html$', TemplateView.as_view(template_name='groups-detail.html'))
)
