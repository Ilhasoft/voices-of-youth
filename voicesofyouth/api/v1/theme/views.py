from rest_framework import permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from voicesofyouth.api.v1.theme.serializers import ThemeSerializer
from voicesofyouth.theme.models import Theme
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
        year_start = self.request.query_params.get('year-start')
        year_end = self.request.query_params.get('year-end')
        if project_id:
            filter_clause['project__id'] = project_id
        if year_start:
            filter_clause['created_on__year__gte'] = year_start
        if year_end:
            filter_clause['created_on__year__lte'] = year_end

        return self.queryset.filter(**filter_clause)

    def retrieve(self, request, pk=None):
        lang = self.request.query_params.get('lang', '').strip()
        theme = get_object_or_404(self.queryset, pk=pk)
        Translation.objects.translate_object(theme, lang)
        serializer = self.serializer_class(theme, context={'request': request})
        return Response(serializer.data)
