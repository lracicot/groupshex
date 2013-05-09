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

class Expense(models.Model):
    """
    A basic expense. Each expense is made by one user, and is added to the user's total expenses, or "Karma"
    """
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Amount'))
    date = models.DateField(auto_now_add=True, verbose_name=_('Date'))
    user = models.ForeignKey(User, verbose_name=_('Buyer'), related_name='expenses')
    
    class Meta:
        ordering = ['-date',]
        get_latest_by = 'date'
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')