from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from voicesofyouth.api.v1.report.serializers import ReportSerializer
from voicesofyouth.report.models import Report
from voicesofyouth.translation.models import Translation


class ReportsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def get_queryset(self):
        filter_clause = {}
        project_id = self.request.query_params.get('project', 0)
        theme_id = self.request.query_params.get('theme', 0)
        if project_id:
            filter_clause['theme__project__id'] = project_id
        if theme_id:
            filter_clause['theme__id'] = theme_id

        return Report.objects.filter(is_active=True,
                                     visible=True,
                                     **filter_clause)

    def retrieve(self, request, pk=None):
        lang = self.request.query_params.get('lang', '').strip()
        report = get_object_or_404(self.queryset, pk=pk)
        Translation.objects.translate_object(report, lang)
        serializer = self.serializer_class(report, context={'request': request})
        return Response(serializer.data)
