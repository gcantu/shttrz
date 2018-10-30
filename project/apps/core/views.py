from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from deals.models import Deal


@login_required
def Home(request):
    return redirect('dashboard:deal-list')


@login_required
def Settings(request):
    return render(request, 'core/settings.html')


@login_required
def Success(request):
    return render(request, 'core/success.html')
