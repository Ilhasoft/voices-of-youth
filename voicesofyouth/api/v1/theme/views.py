from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from voicesofyouth.api.v1.theme.serializers import ThemeSerializer
from voicesofyouth.api.v1.theme.serializers import ThemeTranslationSerializer
from voicesofyouth.theme.models import Theme, ThemeTranslation
from voicesofyouth.translation.models import Translation


class ThemesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given theme.

    list:
    Return a list of all the existing themes by map.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    def get_queryset(self):
        filter_clause = {}
        project_id = self.request.query_params.get('project', 0)
        if project_id:
            filter_clause['project__id'] = project_id

        return Theme.objects.filter(is_active=True,
                                    visible=True,
                                    **filter_clause)

    def retrieve(self, request, pk=None):
        lang = self.request.query_params.get('lang', '').strip()
        theme = get_object_or_404(self.queryset, pk=pk)
        Translation.translate_object(theme, lang)
        serializer = self.serializer_class(theme, context={'request': request})
        return Response(serializer.data)


class ThemeTranslationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ThemeTranslationSerializer
    queryset = ThemeTranslation.objects.all()
    # def get_queryset(self):
    #     return ThemeTranslation.objects.filter(is_active=True,
    #                                            theme__id=self.request.query_params.get('theme', 0))
