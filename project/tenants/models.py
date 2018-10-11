from django.db import models

class tenant(models.Model):
    name = models.CharField(max_length=100)
    subdomain_prefix = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'tenant'
