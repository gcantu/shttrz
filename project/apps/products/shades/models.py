from django.db import models
from django.urls import reverse
from tenants.models import AbstractTenant
from deals.models import Deal
from shutters.utils import custom_round

BOOL_CHOICES = ((True, 'Active'), (False, 'Discontinued'))


class ShadeType(AbstractTenant):
    shade_type = models.CharField(max_length=100)
    status = models.BooleanField(choices=BOOL_CHOICES, default=True)

    def save(self, *args, **kwargs):
        self.shade_type = self.shade_type.capitalize()
        return super(ShadeType, self).save(*args, **kwargs)

    def __str__(self):
        return self.shade_type

    def get_absolute_url(self):
        return reverse('shade-type-detail', kwargs={'pk': self.pk})


class AbstractShade(AbstractTenant):
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

        if 1 < self.shade_type_id < 6:
            p = 14
        elif self.shade_type_id == 6:
            p = 16
        else:
            p = 22

        if w_ft_custom > 7:
            p += 1

        if 3 < h_ft_custom <= 4:
            p = p - 4 if self.shade_type_id == 1 else p - 1

        elif 4 < h_ft_custom <= 5:
            p = p - 6 if self.shade_type_id == 1 else p - 2

        elif 5 < h_ft_custom <= 7:
            p = p - 8 if self.shade_type_id == 1 else p - 3

        elif 7 < h_ft_custom <= 9:
            p = p - 9 if self.shade_type_id == 1 else p - 4

        elif 9 < h_ft_custom <= 11:
            p = p - 10 if self.shade_type_id == 1 else p - 5

        elif 11 < h_ft_custom <= 13:
            p = p - 11 if self.shade_type_id == 1 else p - 6

        elif h_ft_custom > 13:
            p = p - 12 if self.shade_type_id == 1 else p - 7


        tp = (w_ft_custom * h_ft_custom) * p
        return tp

    class Meta:
        abstract = True


class Shade(AbstractShade):
    FRACTION_CHOICES = [(0, ''), (.125, '1/8'), (.25, '1/4'), (.375, '3/8'), (.5, '1/2'), (.625, '5/8'), (.75, '3/4'), (.875, '7/8')]

    deal = models.ForeignKey(Deal, models.SET_NULL, blank=True, null=True)
    product = models.CharField(max_length=10, default='Shades')
    shade_type = models.ForeignKey(ShadeType, models.SET_NULL, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    width_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    height_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    price_per_sq_ft = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.location = self.location.capitalize()
        return super(Shade, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shade-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'shade'
