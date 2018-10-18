from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    subdomain_prefix = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tenant'


# subclass this model to add a foreign key relationship with tenant
class AbstractTenant(models.Model):
    tenant = models.ForeignKey(Tenant, models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True
