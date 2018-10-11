from django.db import models
from django.contrib.auth.models import AbstractUser
from tenants.models import tenant

class User(AbstractUser):
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user'
