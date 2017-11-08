from rest_framework import permissions, viewsets
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from voicesofyouth.api.v1.report.filters import ReportCommentFilter
from voicesofyouth.api.v1.report.filters import ReportFileFilter
from voicesofyouth.api.v1.report.filters import ReportFilter
from voicesofyouth.api.v1.report.filters import ReportMediaFilter
from voicesofyouth.api.v1.report.filters import ReportURLFilter
from voicesofyouth.api.v1.report.paginators import ReportFilesResultsSetPagination
from voicesofyouth.api.v1.report.serializers import ReportCommentsSerializer
from voicesofyouth.api.v1.report.serializers import ReportFilesSerializer
from voicesofyouth.api.v1.report.serializers import ReportMediasSerializer
from voicesofyouth.api.v1.report.serializers import ReportSerializer
from voicesofyouth.api.v1.report.serializers import ReportURLsSerializer
from voicesofyouth.report.models import Report, ReportURL
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile


class ReportsPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = 'page_size'


class ReportsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ReportSerializer
    queryset = Report.objects.prefetch_related('theme', 'created_by', 'files', 'tags').all()
    filter_class = ReportFilter
    pagination_class = ReportsPagination


class ReportCommentsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ReportCommentsSerializer
    queryset = ReportComment.objects.all()
    filter_class = ReportCommentFilter

    def list(self, request, *args, **kwargs):
        url_query = self.request.query_params
        response = None
        if 'report' not in url_query:
            response = Response({}, status=status.HTTP_204_NO_CONTENT)
        return response or super().list(request, *args, **kwargs)


class ReportFilesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ReportFilesSerializer
    queryset = ReportFile.objects.prefetch_related('report', 'created_by').order_by('id').all()
    filter_class = ReportFileFilter
    pagination_class = ReportFilesResultsSetPagination


class ReportURLsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ReportURLsSerializer
    queryset = ReportURL.objects.all()
    filter_class = ReportURLFilter

    def list(self, request, *args, **kwargs):
        url_query = self.request.query_params
        response = None
        if 'report' not in url_query:
            response = Response({}, status=status.HTTP_204_NO_CONTENT)
        return response or super().list(request, *args, **kwargs)


class ReportMediasViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ReportMediasSerializer
    queryset = Report.objects.all()
    filter_class = ReportMediaFilter

    def list(self, request, *args, **kwargs):
        url_query = self.request.query_params
        response = None
        if 'report' not in url_query:
            response = Response({}, status=status.HTTP_204_NO_CONTENT)
        return response or super().list(request, *args, **kwargs)
