from .models import tenant


def hostname_from_request(request):
    return request.get_host().split(':')[0].lower() # split on `:` to remove port


def tenant_from_request(request):
    hostname = hostname_from_request(request)
    subdomain_prefix = hostname.split('.')[0]

    return tenant.objects.filter(subdomain_prefix=subdomain_prefix).first()
