from django.db import models
from tenants.models import AbstractTenant


class Customer(AbstractTenant):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    home_phone = models.CharField(max_length=25, blank=True)
    mobile_phone = models.CharField(max_length=25, blank=True)
    email = models.EmailField(max_length=254, blank=True)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.city = self.city.capitalize()
        return super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('customer-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'customer'
