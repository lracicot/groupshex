from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import Context, loader
from django.http import Http404
from expenses.models import Group, User, Expense, Expense_Shares
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import simplejson
from django.core import serializers
from groupsviews import manage_groups


@login_required()
@ensure_csrf_cookie
def index(request):

    user = User.objects.get(id=request.user.id)
    groups = user.get_groups()

    if groups.count() == 1:
        return __groupboard(request, groups[0], user)

    return redirect('manage_groups')
    #return __manage_groups(user)


@login_required()
@ensure_csrf_cookie
def grouboard(request, group_id):

    user = User.objects.get(id=request.user.id)
    group = Group.objects.get(id=group_id)

    if not group:
        raise Http404

    return __groupboard(group, group, user)


@login_required()
@ensure_csrf_cookie
def add_expense(request):

    user = User.objects.get(id=request.user.id)
    group = Group.objects.get(id=request.POST['group_id'])

    expense = Expense(title=request.POST['title'])
    expense.buyer = user
    expense.group = group
    expense.save()

    for user_share in group.get_users():
        share = Expense_Shares(amount=0, expense=expense, user=user_share)

        if user_share.id == request.user_share.id:
            share.amount = request.POST['amount']

        share.save()

    if request.is_ajax():
        import json

        data = {
            'amount': request.POST['amount'],
            'buyer': user.first_name + ' ' + user.last_name,
            'share': 100,
            'title': expense.title
        }

        return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@login_required()
@ensure_csrf_cookie
def get_expenses(request, group_id):

    group = Group.objects.get(id=group_id)
    data = []

    for expense in group.expenses.all():
        if expense.get_total() > 0:
            data.append({
                'amount': str(expense.get_total()),
                'buyer': expense.buyer.first_name + ' ' + expense.buyer.last_name,
                'share': str(expense.get_total(expense.buyer.id)*100/expense.get_total()),
                'title': expense.title
            })

    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def __groupboard(request, group, user):

    template = loader.get_template('groupboard.html')
    context = Context({
        'groups': user.get_groups(),
        'group': group,
    })

    return HttpResponse(template.render(context))
