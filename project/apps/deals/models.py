from django.db import models
from datetime import datetime, date
from tenants.models import AbstractTenant
from customers.models import Customer
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentMethod(AbstractTenant):
    payment_method = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.payment_method

    def get_absolute_url(self):
        return reverse('payment-method-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'payment_method'


class Deal(AbstractTenant):
    STATUS_CHOICES = (('Active', 'Active'), ('Completed', 'Completed'), ('Deleted', 'Deleted'))

    created_date = models.DateTimeField(default=datetime.today)
    install_date = models.DateField(default=date.today)
    customer = models.ForeignKey(Customer, models.SET_NULL, blank=True, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Active')
    agent = models.ForeignKey(User, related_name='agent', on_delete=models.SET_NULL, blank=True, null=True)
    measured_by = models.ForeignKey(User, related_name='measured_by', on_delete=models.SET_NULL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('deal-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'deal'


class Price(AbstractTenant):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    subtotal = models.FloatField(default=0)
    shutters_subtotal = models.FloatField(default=0)
    blinds_subtotal = models.FloatField(default=0)
    shades_subtotal = models.FloatField(default=0)
    sunscreens_subtotal = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    tax_rate = models.FloatField(default=0.0825)
    tax = models.FloatField(default=0)
    total = models.FloatField(default=0)
    down_payment = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    add_tax = models.BooleanField(default=True)
    credit_card_fee = models.FloatField(default=0)
    credit_card_fee_rate = models.FloatField(default=0.03)
    payment_method = models.ForeignKey(PaymentMethod, models.SET_NULL, blank=True, null=True, default=3)
    check_number = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('price-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'price'
