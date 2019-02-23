from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def Home():
    return redirect(reverse('deals:deal-list', kwargs={'status': 'Active'}))


@login_required
def Success(request):
    return render(request, 'core/success.html')
