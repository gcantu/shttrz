from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def Home(request):
    return render(request, 'core/home.html')


@login_required
def Settings(request):
    return render(request, 'core/settings.html')


@login_required
def Success(request):
    return render(request, 'core/success.html')
