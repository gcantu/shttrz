from shutters.models import Deal
import django_filters


STATUS_CHOICES = (('Active', 'Active'), ('Completed', 'Completed'))

class DealFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)
    date_range = django_filters.DateRangeFilter(field_name='created_date')

    class Meta:
        model = Deal
        fields = ['status',]
