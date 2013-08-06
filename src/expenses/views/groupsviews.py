from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import Context, loader
from django.http import Http404
from expenses.models import Group, User, Expense, Expense_Shares, Membership
from django.utils import simplejson
from django.core import serializers


def manage_groups(request):

    user = User.objects.get(id=request.user.id)
    groups = user.get_groups()

    template = loader.get_template('group_list.html')
    context = Context({
        'groups': groups,
    })

    return HttpResponse(template.render(context))


@login_required()
def get_groups(request):

    user = User.objects.get(id=request.user.id)
    data = []

    for group in user.get_groups():
	    data.append({
	        'id': group.id,
	        'name': group.name
	    })

    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@login_required()
def add_group(request):

    user = User.objects.get(id=request.user.id)

    group = Group(name=request.POST['name'])
    group.save()

    mebership = Membership(group=group, user=user)
    mebership.save()

    if request.is_ajax():
        import json

        data = {
            'id': group.id,
            'name': group.name
        }

        return HttpResponse(simplejson.dumps(data), mimetype="application/json")