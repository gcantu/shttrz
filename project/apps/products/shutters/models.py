from django.db import models
from django.urls import reverse
from tenants.models import AbstractTenant
from .utils import custom_round, as_fraction
from deals.models import Deal

BOOL_CHOICES = ((True, 'Active'), (False, 'Discontinued'))


class Product(AbstractTenant):
    product = models.CharField(max_length=100)
    status = models.BooleanField(choices=BOOL_CHOICES, default=True)

    def save(self, *args, **kwargs):
        self.product = self.product.capitalize()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})


class Stain(AbstractTenant):
    stain = models.CharField(max_length=50)
    status = models.BooleanField(choices=BOOL_CHOICES, default=True)

    def save(self, *args, **kwargs):
        self.stain = self.stain.capitalize()
        return super(Stain, self).save(*args, **kwargs)

    def __str__(self):
        return self.stain

    def get_absolute_url(self):
        return reverse('stain-detail', kwargs={'pk': self.pk})


class HingeColor(AbstractTenant):
    hinge_color = models.CharField(max_length=100)
    status = models.BooleanField(choices=BOOL_CHOICES, default=True)

    def save(self, *args, **kwargs):
        self.hinge_color = self.hinge_color.capitalize()
        return super(HingeColor, self).save(*args, **kwargs)

    def __str__(self):
        return self.hinge_color

    def get_absolute_url(self):
        return reverse('hinge-color-detail', kwargs={'pk': self.pk})


class TiltRod(AbstractTenant):
    tilt_rod = models.CharField(max_length=100)
    status = models.BooleanField(choices=BOOL_CHOICES, default=True)

    def __str__(self):
        return self.tilt_rod

    def get_absolute_url(self):
        return reverse('tilt-rod-detail', kwargs={'pk': self.pk})


class FrameStyle(AbstractTenant):
    frame_style = models.CharField(max_length=50)
    measurement = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.frame_style = self.frame_style.capitalize()
        return super(Frame, self).save(*args, **kwargs)

    def __str__(self):
        return self.frame_style

    def get_absolute_url(self):
        return reverse('frame-detail', kwargs={'pk': self.pk})


class AbstractShutter(AbstractTenant):
    # standard measurements
    # ------------------------------------------------------
    def _stile_width(self):
        return 2

    def _t_post_width(self):
        return 1.25

    # L frame reductions
    # ------------------------------------------------------
    def _width(self):
        w = self.width + self.width_fraction
        return w

    def _height(self):
        h = self.height + self.height_fraction
        return h

    def _get_lframe(self, measure_type):
        measure = self._width() if measure_type == 'width' else self._height()
        deduction = 0.375 if measure_type == 'width' else 0.25 # 3/8 for width, 1/4 for height
        l = (measure - 0.125) if self.mount == 'In' else (measure - deduction)
        return l

    def _l_frame_width(self):
        mt = 'width'
        l = self._get_lframe(mt)
        return l

    def _l_frame_height(self):
        mt = 'height'
        l = self._get_lframe(mt)
        return l

    # rail, louver, stile, tilt rod
    # ------------------------------------------------------
    def _rail(self):
        l_width = self._l_frame_width()
        hinge_offset = 0.125 # 1/8
        opening_offset = 0.0625 # 1/16

        if self.panels == 1:
            reduction = (self.frame_style__measurement*2) + (self._stile_width()*2) + hinge_offset + opening_offset
            rail = l_width - reduction
        elif self.panels == 2:
            reduction = (self.frame_style__measurement*2) + (self._stile_width()*4) + (hinge_offset*2)
            reduction = (reduction + self._t_post_width()) if self.t_post else (reduction + (opening_offset*2))
            rail = (l_width - reduction) / 2
        else: # 4 panels
            reduction = (self.frame_style__measurement*2) + (self._stile_width()*8) + (hinge_offset*4) + (opening_offset*4) + self._t_post_width()
            rail =(l_width - reduction) / 4
        return round(rail, 4)

    def _louver(self):
        louver = self._rail() - 0.0625 # 1/16
        return round(louver, 4)

    def _stile(self):
        Lheight = self._l_frame_height()
        stile = Lheight - 1.75 # 1 3/4
        return round(stile, 4)

    def _tilt_rod(self):
        Trod = self._stile() - 9.875 # 9 7/8
        return round(Trod, 4)

    # Qty
    # ------------------------------------------------------
    def louver_qty(self):
        if self.panels == 1:
            qty = round(((self._stile() - 6) / 3))
        else:
            qty = round(((self._stile() - 10) / 3) * self.panels)
            qty = qty if (qty % 2) == 0 else (qty + 1) # if the number is not even, add 1

        if self.height_divider: # if divider, subtract 1 louver per panel
            qty = qty - self.panels
        return qty

    def rail_qty(self):
        return self.panels * 2

    def stile_qty(self):
        return self.panels * 2

    # calculate material needed
    # ------------------------------------------------------
    def l_frame_material(self):
        material = ((self._l_frame_width() + self._l_frame_height()) / 12) * 2
        return round(material, 4)

    def louver_material(self):
        material = (self._louver() / 12) * self.louver_qty()
        return round(material, 4)

    def rail_material(self):
        material = (self._rail() / 12) * self.rail_qty()
        return round(material, 4)

    def stile_material(self):
        material = (self._stile() / 12) * self.stile_qty()
        return round(material, 4)

    def tilt_rod_material(self):
        material = (self._l_frame_width() / 12) * (self._l_frame_height() / 12)
        return round(material, 4)

    def panel_material(self):
        material = (self._l_frame_height() / 12) * self.panels
        return round(material, 4)

    # calculate hardware needed
    # ------------------------------------------------------
    def total_hinges(self):
        if self._l_frame_height() < 60:
            hinges = self.panels * 2
        elif self._l_frame_height() < 85:
            hinges = self.panels * 3
        else: # < 100
            hinges = self.panels * 4
        return hinges

    def total_magnets(self):
        return self.panels

    def total_screws(self):
        return self.total_hinges() * 6

    # price based on total sq. ft
    # ------------------------------------------------------
    def total_price(self):
        w_ft = self._width()/12
        h_ft = self._height()/12
        w_ft_custom = custom_round(w_ft)
        h_ft_custom = custom_round(h_ft)

        tp = (w_ft_custom * h_ft_custom) * self.price_per_sq_ft
        return tp

    # convert measurements to fraction for display
    # ------------------------------------------------------
    def l_frame_width(self):
        return as_fraction(self._l_frame_width())

    def l_frame_height(self):
        return as_fraction(self._l_frame_height())

    def rail_measure(self):
        return as_fraction(self._rail())

    def louver_measure(self):
        return as_fraction(self._louver())

    def stile_measure(self):
        return as_fraction(self._stile())

    def tilt_rod_measure(self):
        return as_fraction(self._tilt_rod())

    class Meta:
        abstract = True


class Shutter(AbstractShutter):
    FINISH_CHOICES = [('Paint', 'Paint'), ('Stain', 'Stain')]
    LOUVER_CHOICES = [(2.5, '2 1/2'), (3.5, '3 1/2'), (4.5, '4 1/2')]
    MOUNT_CHOICES = [('In', 'Inside'), ('Out', 'Outside')]
    FRAME_CHOICES = [(0, ''), (2, '2 sides'), (3, '3 sides'), (4, '4 sides')]
    HINGE_CHOICES = [('LR', 'Left/Right'), ('L', 'Left'), ('R', 'Right')]
    FRACTION_CHOICES = [(0, ''), (.125, '1/8'), (.25, '1/4'), (.375, '3/8'), (.5, '1/2'), (.625, '5/8'), (.75, '3/4'), (.875, '7/8')]

    deal = models.ForeignKey(Deal, models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True)
    finish = models.CharField(max_length=5, choices=FINISH_CHOICES, blank=True, null=True)
    stain = models.ForeignKey(Stain, models.SET_NULL, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    louver = models.FloatField(choices=LOUVER_CHOICES, blank=True, null=True)
    mount = models.CharField(max_length=3, choices=MOUNT_CHOICES, blank=True)
    frame = models.IntegerField(choices=FRAME_CHOICES, default=0)
    frame_style = models.ForeignKey(FrameStyle, models.SET_NULL, blank=True, null=True)
    panels = models.IntegerField(blank=True, null=True)
    t_post = models.IntegerField(blank=True, null=True)
    hinges = models.CharField(max_length=2, choices=HINGE_CHOICES, blank=True)
    hinge_color = models.ForeignKey(HingeColor, models.SET_NULL, blank=True, null=True)
    tilt_rod = models.ForeignKey(TiltRod, models.SET_NULL, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    height_divider = models.IntegerField(blank=True, null=True)
    width_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    height_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    height_divider_fraction = models.FloatField(choices=FRACTION_CHOICES, default=0)
    price_per_sq_ft = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.location = self.location.capitalize()
        self.color = self.color.capitalize()

        # use L frame for stain and Z frame for paint
        self.frame_style_id = 1 if self.finish == 'Stain' else 2
        return super(Shutter, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('shutter-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'shutter'



class Material(AbstractTenant):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, primary_key=True)
    l_frame_material = models.IntegerField(default=0)
    louver_material = models.IntegerField(default=0)
    rail_material = models.IntegerField(default=0)
    stile_material = models.IntegerField(default=0)
    tilt_rod_material = models.IntegerField(default=0)
    panel_material = models.IntegerField(default=0)
    total_hinges = models.IntegerField(default=0)
    total_magnets = models.IntegerField(default=0)
    total_screws = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('material-detail', kwargs={'pk': self.pk})
