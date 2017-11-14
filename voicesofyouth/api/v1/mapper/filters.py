from django_filters import rest_framework as filters

from voicesofyouth.user.models import MapperUser


class MapperUserFilter(filters.FilterSet):
    theme = filters.NumberFilter(name='groups__theme_mappers', help_text='Filter mappers by theme id.')

    class Meta:
        model = MapperUser
        fields = ('theme',)
