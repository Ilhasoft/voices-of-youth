from django.db.models.query_utils import Q

from rest_framework import permissions, viewsets, mixins
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from voicesofyouth.api.v1.report.filters import ReportCommentFilter
from voicesofyouth.api.v1.report.filters import ReportFileFilter
from voicesofyouth.api.v1.report.filters import ReportFilter
from voicesofyouth.api.v1.report.paginators import ReportFilesResultsSetPagination
from voicesofyouth.api.v1.report.serializers import ReportCommentsSerializer
from voicesofyouth.api.v1.report.serializers import ReportFilesSerializer
from voicesofyouth.api.v1.report.serializers import ReportSerializer
from voicesofyouth.api.v1.report.serializers import ReportNotifictionsSerializer
from voicesofyouth.report.models import Report
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile
from voicesofyouth.report.models import ReportNotification
from voicesofyouth.report.models import NOTIFICATION_STATUS_APPROVED
from voicesofyouth.report.models import NOTIFICATION_STATUS_NOTAPPROVED
from voicesofyouth.report.models import NOTIFICATION_STATUS_PENDING
from voicesofyouth.report.models import NOTIFICATION_ORIGIN_COMMENT
from voicesofyouth.report.models import REPORT_STATUS_APPROVED


class ReportsPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = 'page_size'


class ReportsViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
    Returns a list of reports. You can filter reports by project, by theme, by mapper or by status.

    create:
    Create a new report. Only Mappers can do that.

    read:
    Returns a report data.

    update:
    Update report.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ReportSerializer
    queryset = Report.objects.all().filter(theme__visible=True).prefetch_related('theme', 'created_by', 'files', 'tags').all()
    filter_class = ReportFilter
    pagination_class = ReportsPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            tags=self.request.data.get('tags', []),
            urls=self.request.data.get('urls', []))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            tags=self.request.data.get('tags', []),
            urls=self.request.data.get('urls', []))

        return Response(serializer.data)


class ReportCommentsViewSet(viewsets.ModelViewSet):
    """
    list:
    Returns a list of approved comments by Report.

    create:
    Create a comment, the comment is sent to moderation.

    read:
    Returns a comment data.

    update:
    Update a comment.

    delete:
    Delete a comment.
    """
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ReportCommentsSerializer
    queryset = ReportComment.objects.approved().order_by('created_on')
    filter_class = ReportCommentFilter

    def list(self, request, *args, **kwargs):
        url_query = self.request.query_params
        response = None
        if 'report' not in url_query:
            response = Response({}, status=status.HTTP_204_NO_CONTENT)
        return response or super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        headers = self.get_success_headers(serializer.data)

        notification = ReportNotification.objects.filter(report=comment.report).filter(origin=NOTIFICATION_ORIGIN_COMMENT).first()

        if notification is None:
            ReportNotification.objects.create(
                status=NOTIFICATION_STATUS_PENDING,
                read=False,
                origin=NOTIFICATION_ORIGIN_COMMENT,
                report=comment.report,
                created_by=comment.report.created_by,
                modified_by=comment.report.modified_by,
            )
        else:
            notification.status = NOTIFICATION_STATUS_PENDING
            notification.read = False
            notification.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReportFilesViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """
    list:
    Returns the list of report files.

    create:
    Send a file. Image: jpg, png, gif. Video webm, mp4

    delete:
    Delete file.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ReportFilesSerializer
    queryset = ReportFile.objects.prefetch_related('report', 'created_by').order_by('-created_on').all()
    filter_class = ReportFileFilter
    pagination_class = ReportFilesResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(report__status=REPORT_STATUS_APPROVED))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.report.created_by == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response('Permission denied', status=status.HTTP_403_FORBIDDEN)


class ReportSearchViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """
    Returns a list of reports that are searched by name, theme, or tags. Example: /report-search/?query=find_it&project=project_id
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def list(self, request, *args, **kwargs):
        query = self.request.query_params.get('query', None)
        project = self.request.query_params.get('project', None)

        if query and project:
            queryset = self.get_queryset() \
                .filter(status=REPORT_STATUS_APPROVED) \
                .filter(theme__project__id=project) \
                .filter(Q(theme__name__icontains=query) | Q(name__icontains=query) | Q(tagged_items__tag__name__icontains=query)).distinct()

            if len(queryset) > 0:
                return Response(self.get_serializer(queryset, many=True).data)

        return Response({})


class ReportNotificationViewSet(
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = ReportNotification.objects.all()
    serializer_class = ReportNotifictionsSerializer

    def list(self, request, *args, **kwargs):
        project = self.request.query_params.get('project', None)
        queryset = self.get_queryset() \
            .filter(report__created_by_id=request.user.id) \
            .filter(status__in=[NOTIFICATION_STATUS_APPROVED, NOTIFICATION_STATUS_NOTAPPROVED]) \
            .filter(read=False).distinct()

        if project:
            queryset = queryset.filter(report__theme__project__id=project)

        if len(queryset) > 0:
            return Response(self.get_serializer(queryset, many=True).data)

        return Response([])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        serializer.save(read=True)

        return Response(serializer.data)
