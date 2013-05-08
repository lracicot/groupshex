from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    description = models.TextField(verbose_name=_('Description'), blank=True)
    amout = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Amount'))
    date = models.DateField(auto_now_add=True, verbose_name=_('Date'))
    user = models.ForeignKey(User, verbose_name=_('Buyer'))