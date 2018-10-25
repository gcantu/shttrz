from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from deals.models import Deal


@login_required
def Home(request):
    deals = Deal.objects.filter(is_deleted=False)
    return render(request, 'core/home.html', {'deals': deals})


@login_required
def Settings(request):
    return render(request, 'core/settings.html')


@login_required
def Success(request):
    return render(request, 'core/success.html')
