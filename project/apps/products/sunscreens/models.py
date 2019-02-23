from django.db import models
from django.urls import reverse
from tenants.models import AbstractTenant
from deals.models import Deal
from shutters.utils import custom_round

BOOL_CHOICES = ((True, 'Active'), (False, 'Discontinued'))


class SunscreenType(AbstractTenant):
    sunscreen_type = models.CharField(max_length=100)
    status = models.BooleanField(choices=BOOL_CHOICES, default=True)

    def save(self, *args, **kwargs):
        self.sunscreen_type = self.sunscreen_type.capitalize()
        return super(SunscreenType, self).save(*args, **kwargs)

    def __str__(self):
        return self.sunscreen_type

    def get_absolute_url(self):
        return reverse('sunscreen-type-detail', kwargs={'pk': self.pk})


class AbstractSunscreen(AbstractTenant):
    # measurements
    # ------------------------------------------------------
    def _width(self):
        w = self.width + self.width_fraction
        return w

    def _height(self):
        h = self.height + self.height_fraction
        return h

    # price based on total sq. ft
    # ------------------------------------------------------
    def total_price(self):
        w_ft = self._width()/12
        h_ft = self._height()/12
        w_ft_custom = custom_round(w_ft)
        h_ft_custom = custom_round(h_ft)

        if self.sunscreen_type_id == 1:
            p = (w_ft_custom + h_ft_custom) * 8
        elif self.sunscreen_type_id == 2:
            p = (w_ft_custom + h_ft_custom) * 10
        elif self.sunscreen_type_id == 3:
            p = (w_ft_custom + h_ft_custom) * 12

        tp = p
        return tp

    class Meta:
        abstract = True


class Sunscreen(AbstractSunscreen):
    FRACTION_CHOICES = [(0, ''), (.125, '1/8'), (.25, '1/4'), (.375, '3/8'), (.5, '1/2'), (.625, '5/8'), (.75, '3/4'), (.875, '7/8')]
    STATUS_CHOICES = (('Approved', 'Approved'), ('Canceled', 'Canceled'))

    deal = models.ForeignKey(Deal, models.SET_NULL, blank=True, null=True)
    product = models.CharField(max_length=10, default='Sunscreens')
    sunscreen_type = models.ForeignKey(SunscreenType, models.SET_NULL, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    width_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    height_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    price_per_sq_ft = models.FloatField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Approved')

    def save(self, *args, **kwargs):
        self.location = self.location.capitalize()
        return super(Sunscreen, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sunscreen-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'sunscreen'
