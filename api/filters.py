from django_filters import rest_framework

from .models import Statistic


class DateFilter(rest_framework.FilterSet):
    date_from = rest_framework.DateTimeFilter(field_name='date', lookup_expr='gte')
    date_to = rest_framework.DateTimeFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Statistic
        fields = ['date_from', 'date_to']
