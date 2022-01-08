from rest_framework import filters

from .validators import validate_date_format


class DateIntervalFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        start_date = request.GET['from'] if "from" in request.GET else None
        end_date = request.GET['to'] if "to" in request.GET else None

        if start_date or end_date:
            if start_date:
                validate_date_format(start_date)
                if end_date:
                    validate_date_format(end_date)
                    return queryset.filter(date__gte=start_date).exclude(date__gt=end_date)
                return queryset.filter(date__gte=start_date)
            return queryset.filter(date__lte=end_date)
        return queryset
