from rest_framework import permissions, viewsets
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from voicesofyouth.api.v1.report.filters import ReportCommentFilter
from voicesofyouth.api.v1.report.filters import ReportFileFilter
from voicesofyouth.api.v1.report.filters import ReportFilter
from voicesofyouth.api.v1.report.paginators import ReportFilesResultsSetPagination
from voicesofyouth.api.v1.report.serializers import ReportCommentsSerializer
from voicesofyouth.api.v1.report.serializers import ReportFilesSerializer
from voicesofyouth.api.v1.report.serializers import ReportMediasSerializer
from voicesofyouth.api.v1.report.serializers import ReportSerializer
from voicesofyouth.api.v1.report.serializers import ReportURLsSerializer
from voicesofyouth.report.models import Report, ReportURL
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile
from voicesofyouth.translation.models import Translation


class ReportsPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = 'page_size'


class ReportsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    filter_class = ReportFilter
    pagination_class = ReportsPagination

    def retrieve(self, request, pk=None):
        lang = self.request.query_params.get('lang', '').strip()
        report = get_object_or_404(self.queryset, pk=pk)
        Translation.objects.translate_object(report, lang)
        serializer = self.serializer_class(report, context={'request': request})
        return Response(serializer.data)


class ReportCommentsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ReportCommentsSerializer
    queryset = ReportComment.objects.all()
    filter_class = ReportCommentFilter

    def list(self, request, *args, **kwargs):
        url_query = self.request.query_params
        if 'report' not in url_query:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return super().list(request, *args, **kwargs)


class ReportFilesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ReportFilesSerializer
    queryset = ReportFile.objects.all()
    filter_class = ReportFileFilter
    pagination_class = ReportFilesResultsSetPagination


class ReportURLsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
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


class ReportMediasViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
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
