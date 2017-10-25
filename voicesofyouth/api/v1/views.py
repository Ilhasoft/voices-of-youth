from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from voicesofyouth.api.v1.serializers import TagSerializer
from voicesofyouth.maps.models import Map
from voicesofyouth.reports.models import Report
from voicesofyouth.tag.models import Tag
from voicesofyouth.theme.models import Theme
from voicesofyouth.translation.models import Translation
from voicesofyouth.users.models import User
from .serializers import CommentSerializer
from .serializers import MapSerializer
from .serializers import ReportAndMediasSerializer
from .serializers import ReportSerializer
from .serializers import UserSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Only list tags related with theme.

    User cannot create tags directly via API because tags cannot exists without related data. e.g. When create new
    Theme, if user send a list of tags(comma separated) the system will created these tags automatically.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TagSerializer

    def get_queryset(self):
        theme = get_object_or_404(Theme, pk=self.request.query_params.get('theme', 0))
        return Tag.objects.filter(object_id=theme.id)


class MapsEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given map and related themes.

    list:
    Return a list of all the existing maps.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = MapSerializer
    queryset = Map.objects.all()

    # def get_queryset(self):
    #     return Map.objects.filter(is_active=True).filter(id=self.kwargs['pk'])
    #
    # def retrieve(self, request, *args, **kwargs):
    #     self.serializer_class = MapAndThemesSerializer
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)


class ReportsEndPoint(viewsets.ReadOnlyModelViewSet,
                      mixins.CreateModelMixin):
    """
    create:
    Create a new report.

    retrieve:
    Return the given report.

    list:
    Return a list of all the existing reports
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    # def retrieve(self, request, *args, **kwargs):
    #     """
    #     todos do projeto
    #     todos por tema
    #     e o proprio report
    #     """
    #     self.serializer_class = ReportAndMediasSerializer
    #     project_id = kwargs.get('project')
    #     theme_id = kwargs.get('theme')
    #     instance = Report.objects.get(pk=kwargs.get('pk'))
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
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

class CommentsEndPoint(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """
    create:
    Create a new comment.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)


class UsersEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given theme.

    list:
    Return a list of all the existing themes by map.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all().filter(is_active=True)
