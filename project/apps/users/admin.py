from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group
from tenants.utils import tenant_from_request


class CustomUserAdmin(UserAdmin):
    # only query users that belong to active tenant
    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        tenant = tenant_from_request(request)
        return qs.filter(tenant=tenant)


admin.site.register(User, CustomUserAdmin)

admin.site.unregister(Group) # remove Group from admin site
