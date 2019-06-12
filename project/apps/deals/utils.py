from .models import Deal
import django_filters

class DealFilter(django_filters.FilterSet):
    date_range = django_filters.DateRangeFilter(field_name='created_date')

    class Meta:
        model = Deal
        fields = ['created_date',]
