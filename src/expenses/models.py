from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Expense(models.Model):
    """
    A basic expense. Each expense is made by one user, and is added to the user's total expenses, or "Karma"
    """
    description = models.TextField(verbose_name=_('Description'), blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Amount'))
    date = models.DateField(auto_now_add=True, verbose_name=_('Date'))
    user = models.ForeignKey(User, verbose_name=_('Buyer'))
    
    class Meta:
        ordering = ['-date',]
        get_latest_by = 'date'
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')
