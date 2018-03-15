from rest_framework import permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from voicesofyouth.api.v1.theme.filters import ThemeFilter
from voicesofyouth.api.v1.theme.serializers import ThemeSerializer
from voicesofyouth.theme.models import Theme
from voicesofyouth.translation.models import Translation


class ThemesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return a list of themes. You can filter reports by project, by mapper or by start/end year.

    retrieve:
    Return a specific theme.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Theme.objects.all().filter(visible=True)
    serializer_class = ThemeSerializer
    filter_class = ThemeFilter

    def retrieve(self, request, pk=None):
        lang = self.request.query_params.get('lang', '').strip()
        theme = get_object_or_404(self.queryset, pk=pk)
        Translation.objects.translate_object(theme, lang)
        serializer = self.serializer_class(theme, context={'request': request})
        return Response(serializer.data)
