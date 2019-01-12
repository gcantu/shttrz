from django.db import models
from django.urls import reverse
from tenants.models import AbstractTenant
from deals.models import Deal
from shutters.utils import custom_round

BOOL_CHOICES = ((True, 'Active'), (False, 'Discontinued'))


class BlindType(AbstractTenant):
    blind_type = models.CharField(max_length=100)
    status = models.BooleanField(choices=BOOL_CHOICES, default=True)

    def save(self, *args, **kwargs):
        self.blind_type = self.blind_type.capitalize()
        return super(BlindType, self).save(*args, **kwargs)

    def __str__(self):
        return self.blind_type

    def get_absolute_url(self):
        return reverse('blind-type-detail', kwargs={'pk': self.pk})


class FauxWoodStyle(AbstractTenant):
    faux_wood_style = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.faux_wood_style = self.faux_wood_style.capitalize()
        return super(FauxWoodStyle, self).save(*args, **kwargs)

    def __str__(self):
        return self.faux_wood_style

    def get_absolute_url(self):
        return reverse('faux-wood-detail', kwargs={'pk': self.pk})


class AbstractBlind(AbstractTenant):
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

        if self.blind_type_id == 1:
            p = 7

            if w_ft_custom < 2:
                p += 10

            if w_ft_custom > 5:
                p -= 1

            if 4 < h_ft_custom <= 6:
                p -= 1
            elif h_ft_custom > 7:
                p -= 2

        elif self.blind_type_id == 2:
            p = 4

            if w_ft_custom <= 4 or h_ft_custom <= 5:
                p += 1

            if h_ft_custom <= 4:
                p += 1

            if h_ft_custom <=4 and w_ft_custom <=3:
                p += 1

            if h_ft_custom <=3 and w_ft_custom <=3:
                p += 1

            if h_ft_custom <= 2:
                p += 1

            if h_ft_custom <=2 and w_ft_custom <=4:
                p += 1

        elif self.blind_type_id == 3:
            p = 6

            if w_ft_custom <= 3:
                p += 1

            if h_ft_custom <= 5:
                p += 1

            if h_ft_custom <= 2:
                p += 4

        elif self.blind_type_id >= 4:
            p = 3

            if w_ft_custom <= 3 or h_ft_custom <= 7:
                p += 1

            if h_ft_custom <= 5 and w_ft_custom <= 3:
                p += 1

            if h_ft_custom <= 3:
                p += 1

            if h_ft_custom <= 2 and w_ft_custom <= 5:
                p += 1

            if h_ft_custom <= 7 and w_ft_custom <= 2:
                p += 1

            if h_ft_custom <= 2 and w_ft_custom <= 4:
                p += 1

        tp = (w_ft_custom * h_ft_custom) * p

        if self.blind_type_id == 5:
            tp += 3

        return tp

    class Meta:
        abstract = True


class Blind(AbstractBlind):
    FRACTION_CHOICES = [(0, ''), (.125, '1/8'), (.25, '1/4'), (.375, '3/8'), (.5, '1/2'), (.625, '5/8'), (.75, '3/4'), (.875, '7/8')]

    deal = models.ForeignKey(Deal, models.SET_NULL, blank=True, null=True)
    product = models.CharField(max_length=10, default='Blinds')
    blind_type = models.ForeignKey(BlindType, models.SET_NULL, blank=True, null=True)
    faux_wood_style = models.ForeignKey(FauxWoodStyle, models.SET_NULL, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    width_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    height_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    price_per_sq_ft = models.FloatField(default=0)
    default_style = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.location = self.location.capitalize()
        return super(Blind, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blind-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'blind'
