from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from deals.models import Deal


@login_required
def Home(request):
    return redirect(reverse('dashboard:deal-list', kwargs={'status': 'All'}))


@login_required
def Settings(request):
    return render(request, 'core/settings.html')


@login_required
def Success(request):
    return render(request, 'core/success.html')
