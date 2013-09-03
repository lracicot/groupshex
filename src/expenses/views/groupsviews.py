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
def get_group(request, group_id):

    user = User.objects.get(id=request.user.id)
    data = {'id': '', 'name': ''}

    for group in user.get_groups():

        if group.id == int(group_id):
            data = {'id': group.id, 'name': group.name}

    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@login_required()
def add_member(request, group_id, member_id):

    user = User.objects.get(id=request.user.id)
    member = User.objects.get(id=member_id)
    data = {'id': '', 'name': ''}

    for group in user.get_groups():

        if group.id == int(group_id):
            m = Membership(user=member, group=group)
            m.save()

    return HttpResponse('', mimetype="application/json")


@login_required()
def remove_member(request, group_id, member_id):

    user = User.objects.get(id=request.user.id)
    member = User.objects.get(id=member_id)
    data = {'id': '', 'name': ''}

    for group in user.get_groups():

        if group.id == int(group_id):
            membership = Membership.objects.filter(user=member, group=group)
            membership.delete()

    return HttpResponse('', mimetype="application/json")


@login_required()
def get_members(request, group_id):

    user = User.objects.get(id=request.user.id)
    data = []

    for group in user.get_groups():
        if group.id == int(group_id):
            for member in group.get_users():
                data.append({'id': member.id, 'name': member.first_name + ' ' + member.last_name})

    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@login_required()
def get_not_members(request, group_id):

    user = User.objects.get(id=request.user.id)
    members_id = []
    data = []

    for group in user.get_groups():
        if group.id == int(group_id):
            for member in group.get_users():
                members_id.append(member.id)

    for user in User.objects.exclude(id__in=members_id).filter(first_name__icontains=request.POST['term']):
        data.append({'id': user.id, 'name': user.first_name + ' ' + user.last_name});

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