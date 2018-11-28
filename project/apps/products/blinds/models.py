from django.db import models
from django.urls import reverse
from tenants.models import AbstractTenant
from deals.models import Deal

class AbstractBlind(AbstractTenant):
    # measurements
    # ------------------------------------------------------
    def _width(self):
        w = self.width + self.width_fraction
        return w

    def _height(self):
        h = self.height + self.height_fraction
        return h

    class Meta:
        abstract = True


class Blind(AbstractBlind):
    FRACTION_CHOICES = [(0, ''), (.125, '1/8'), (.25, '1/4'), (.375, '3/8'), (.5, '1/2'), (.625, '5/8'), (.75, '3/4'), (.875, '7/8')]

    deal = models.ForeignKey(Deal, models.SET_NULL, blank=True, null=True)
    product = models.CharField(max_length=10, default='Blinds')
    # blind_type = models.ForeignKey(BlindType, models.SET_NULL, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    width_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    height_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    price_per_sq_ft = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.location = self.location.capitalize()
        return super(Blind, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blind-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'blind'
