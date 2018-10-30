from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shutters.models import Deal
import django_filters
from django import forms

STATUS_CHOICES = (('Active', 'Active'), ('Completed', 'Completed'), ('Deleted', 'Deleted'))


class DealFilter(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(choices=STATUS_CHOICES, widget=forms.CheckboxSelectMultiple)
    date_range = django_filters.DateRangeFilter(field_name='created_date')

    class Meta:
        model = Deal
        fields = ['status',]


@login_required
def deal_list(request):
    filter = DealFilter(request.GET, queryset=Deal.objects.all())
    return render(request, 'core/home.html', {'filter': filter})
