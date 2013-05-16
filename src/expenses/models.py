from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User as DjangoUser

class UserManager(models.Manager):
    """
    Automatically applies select_related on the User model so its expenses are selected too
    """
    def get_query_set(self):
        return super(UserManager, self).get_query_set().select_related('expenses')

class User(DjangoUser):
    """
    Extends the default User model to add expense-related functionnality
    """
    objects = UserManager()

    class Meta:
        proxy = True

class Group(models.Model):
    """
    A group is a number of person sharing expenses for a particular purpose
    """
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    users = models.ManyToManyField(User, verbose_name=_('User'), related_name='groups', through='Membership')

class Membership(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    date_joined = models.DateField(verbose_name=_('Date joined'))

class Expense(models.Model):
    """
    A basic expense. Each expense is made by one user, and is added to the user's total expenses, or "Karma"
    """
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Amount'))
    date = models.DateField(auto_now_add=True, verbose_name=_('Date'))
    buyer = models.ForeignKey(User, verbose_name=_('Buyer'), related_name='expenses')
    sharers = models.ManyToManyField(User, verbose_name=_('Sharers'), related_name='involvedExpenses', through='ExpensesUsers')
    group = models.ForeignKey(Group, verbose_name=_('Group'), related_name='expenses')
    
    class Meta:
        ordering = ['-date',]
        get_latest_by = 'date'
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

class ExpensesUsers(models.Model):
    user = models.ForeignKey(User)
    expense = models.ForeignKey(Expense)
    paid = models.BooleanField(verbose_name=_('Paid'))
    paid_amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Amount'))