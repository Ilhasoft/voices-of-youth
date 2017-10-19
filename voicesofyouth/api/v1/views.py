from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from voicesofyouth.maps.models import Map
from voicesofyouth.reports.models import Report
from voicesofyouth.themes.models import Theme, ThemeTags
from voicesofyouth.users.models import User
from .serializers import MapSerializer, ThemeSerializer
from .serializers import ReportSerializer, ReportAndMediasSerializer, CommentSerializer
from .serializers import TagSerializer
from .serializers import ThemeAndReportsSerializer, UserSerializer


class TagsEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all the existing tags. Required Theme ID
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = ThemeTags.objects.all().filter(theme__id=self.request.query_params.get('theme', None))
        return map(lambda tag: tag.tag, queryset)


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


class ThemesEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given theme.

    list:
    Return a list of all the existing themes by map.
    """
    serializer_class = ThemeSerializer

    def get_queryset(self):
        return Theme.objects.all().filter(is_active=True).filter(visible=True).filter(project__id=self.request.query_params.get('project', 0))

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ThemeAndReportsSerializer
        instance = Theme.objects.get(pk=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ReportAndMediasSerializer
        instance = Report.objects.get(pk=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
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
