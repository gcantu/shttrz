from django.db import models
from django.contrib.auth.models import AbstractUser
from tenants.models import Tenant

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'user'
