from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shutters.models import Deal
import django_filters
from django import forms

STATUS_CHOICES = (('Active', 'Active'), ('Completed', 'Completed'))


class DealFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)
    date_range = django_filters.DateRangeFilter(field_name='created_date')

    class Meta:
        model = Deal
        fields = ['status',]


@login_required
def deal_list(request, status):
    if status == 'Deleted':
        filter = DealFilter(request.GET, queryset=Deal.objects.filter(status='Deleted'))
        return render(request, 'deals/deleted_deals_list.html', {'filter': filter, 'status': status})
    else:
        filter = DealFilter(request.GET, queryset=Deal.objects.exclude(status='Deleted'))
        return render(request, 'core/home.html', {'filter': filter, 'status': status})
