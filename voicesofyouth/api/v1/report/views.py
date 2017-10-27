from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from voicesofyouth.api.v1.report.serializers import ReportCommentsSerializer, ReportFilesSerializer, \
    ReportURLsSerializer, ReportMediasSerializer
from voicesofyouth.api.v1.report.serializers import ReportSerializer
from voicesofyouth.report.models import Report, ReportURL
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile
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


class ReportCommentsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReportCommentsSerializer
    queryset = ReportComment.objects.all()

    def list(self, request, *args, **kwargs):
        query = {}
        url_query = self.request.query_params
        query_status = status.HTTP_200_OK
        if 'report' in url_query:
            query['report__id'] = url_query.get('report')
            qs = self.queryset.filter(**query)
        else:
            qs = {}
            query_status = status.HTTP_204_NO_CONTENT
        serializer = self.serializer_class(qs, many=True, context={'request': request})
        return Response(serializer.data, status=query_status)


class ReportFilesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReportFilesSerializer
    queryset = ReportFile.objects.all()

    def list(self, request, *args, **kwargs):
        query = {}
        url_query = self.request.query_params
        query_status = status.HTTP_200_OK
        if 'report' in url_query:
            query['report__id'] = url_query.get('report')
            qs = self.queryset.filter(**query)
        else:
            qs = {}
            query_status = status.HTTP_204_NO_CONTENT
        serializer = self.serializer_class(qs, many=True, context={'request': request})
        return Response(serializer.data, status=query_status)


class ReportURLsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReportURLsSerializer
    queryset = ReportURL.objects.all()

    def list(self, request, *args, **kwargs):
        query = {}
        url_query = self.request.query_params
        query_status = status.HTTP_200_OK
        if 'report' in url_query:
            query['report__id'] = url_query.get('report')
            qs = self.queryset.filter(**query)
        else:
            qs = {}
            query_status = status.HTTP_204_NO_CONTENT
        serializer = self.serializer_class(qs, many=True, context={'request': request})
        return Response(serializer.data, status=query_status)


class ReportMediasViewSet(viewsets.ViewSet):
    serializer_class = ReportMediasSerializer
    queryset = Report.objects.all()

    def list(self, request):
        query = {}
        url_query = self.request.query_params
        query_status = status.HTTP_200_OK
        if 'report' in url_query:
            query['id'] = url_query.get('report')
            qs = self.queryset.filter(**query)
        else:
            qs = {}
            query_status = status.HTTP_204_NO_CONTENT
        serializer = self.serializer_class(qs, context={'request': request}, many=True)
        return Response(serializer.data, status=query_status)
