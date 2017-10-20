from rest_framework import viewsets

from voicesofyouth.api.v1.theme.serializers import ThemeSerializer
from voicesofyouth.theme.models import Theme


class ThemesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given theme.

    list:
    Return a list of all the existing themes by map.
    """
    serializer_class = ThemeSerializer

    def get_queryset(self):
        return Theme.objects.filter(is_active=True,
                                    visible=True,
                                    project__id=self.request.query_params.get('project', 0))

    # def retrieve(self, request, *args, **kwargs):
    #     self.serializer_class = ThemeAndReportsSerializer
    #     instance = Theme.objects.get(pk=kwargs.get('pk'))
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
