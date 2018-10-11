from django.contrib.auth.backends import ModelBackend
from tenants.utils import tenant_from_request
from django.contrib.auth import get_user_model


UserModel = get_user_model()

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user) and self.valid_subdomain(request, user):
                return user

    def valid_subdomain(self, request, user): # users can only access the app through their company's subdomain
        """
        Check if user is using allowed subdomain
        """
        tenant = tenant_from_request(request)
        tenant_id = tenant.id
        user_tenant_id = user.tenant_id

        if (tenant_id == user_tenant_id):
            is_valid = 1
        else:
            is_valid = None
        return is_valid
