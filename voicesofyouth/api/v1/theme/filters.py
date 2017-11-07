from django_filters import rest_framework as filters

from voicesofyouth.theme.models import Theme


class ThemeFilter(filters.FilterSet):
    year_start = filters.NumberFilter('created_on__year',
                                      lookup_expr='gte',
                                      label='Start year',
                                      help_text='Get all themes that has been created from this year.')
    year_end = filters.NumberFilter('created_on__year',
                                    lookup_expr='lte',
                                    label='End year',
                                    help_text='Get all themes that has been created until this year.')
    project = filters.NumberFilter(help_text='Filter themes by project id.')
    user = filters.NumberFilter('mappers_group__user', help_text='Filter themes that user id is associated.')

    class Meta:
        model = Theme
        fields = ('project', )
