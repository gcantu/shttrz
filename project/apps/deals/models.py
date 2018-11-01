from django.db import models
from datetime import datetime, date
from tenants.models import AbstractTenant
from customers.models import Customer


class Deal(AbstractTenant):
    created_date = models.DateTimeField(default=datetime.today)
    install_date = models.DateField(default=date.today)
    customer = models.ForeignKey(Customer, models.SET_NULL, blank=True, null=True)
    notes = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('deal-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'deal'


class Price(AbstractTenant):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    subtotal = models.FloatField(default=0)
    tax_rate = models.FloatField(default=0.0825)
    tax = models.FloatField(default=0)
    total = models.FloatField(default=0)
    down_payment = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    add_tax = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('price-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'price'
