from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import Context, loader
from django.http import Http404
from expenses.models import Group, User


@login_required()
def index(request):

    user = User.objects.get(id=request.user.id)
    groups = user.get_groups()

    if groups.count() == 1:
        return __groupboard(groups[0], user)

    return __manage_groups(user)


@login_required()
def grouboard(request, group_id):

    user = User.objects.get(id=request.user.id)
    group = Group.objects.get(id=group_id)

    if not group:
        raise Http404

    return __groupboard(group, user)


@login_required()

    

def __groupboard(group, user):

    template = loader.get_template('groupboard.html')
    context = Context({
        'groups': user.get_groups(),
        'group': group,
    })

    return HttpResponse(template.render(context))

def __manage_group(user, groups):

    template = loader.get_template('group_list.html')
    context = Context({
        'groups': groups,
    })

    return HttpResponse(template.render(context))
