from django.db import models
from django.contrib.auth.models import AbstractUser
from tenants.models import Tenant

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        db_table = 'user'
