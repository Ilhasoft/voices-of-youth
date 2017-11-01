from django_filters import rest_framework as filters

from voicesofyouth.theme.models import Theme


class ThemeFilter(filters.FilterSet):
    year_start = filters.NumberFilter('created_on__year', lookup_expr='gte', label='Start year')
    year_end = filters.NumberFilter('created_on__year', lookup_expr='lte', label='End year')

    class Meta:
        model = Theme
        fields = ('project', 'created_on')
