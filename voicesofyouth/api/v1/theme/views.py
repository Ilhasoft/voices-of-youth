from rest_framework import viewsets, permissions

from voicesofyouth.api.v1.theme.serializers import ThemeSerializer
from voicesofyouth.api.v1.theme.serializers import ThemeTranslationSerializer
from voicesofyouth.theme.models import Theme, ThemeTranslation


class ThemesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given theme.

    list:
    Return a list of all the existing themes by map.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ThemeSerializer

    def get_queryset(self):
        return Theme.objects.filter(is_active=True,
                                    visible=True,
                                    project__id=self.request.query_params.get('project', 0))


class ThemeTranslationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ThemeTranslationSerializer
    queryset = ThemeTranslation.objects.all()
    # def get_queryset(self):
    #     return ThemeTranslation.objects.filter(is_active=True,
    #                                            theme__id=self.request.query_params.get('theme', 0))
