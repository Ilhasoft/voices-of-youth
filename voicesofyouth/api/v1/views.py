from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from voicesofyouth.tags.models import Tag
from voicesofyouth.projects.models import Project
from voicesofyouth.maps.models import Map
from voicesofyouth.themes.models import Theme
from voicesofyouth.users.models import User

from .serializers import TagSerializer, ProjectSerializer
from .serializers import MapSerializer, MapAndThemesSerializer, ThemeSerializer, UserSerializer


class ProjectsEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given project.

    list:
    Return a list of all the existing projects.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Project.objects.all().filter(is_active=True)
    serializer_class = ProjectSerializer


class TagsEndPoint(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    retrieve:
    Return the given tag.

    list:
    Return a list of all the existing tags.

    create:
    Create a new tag instance.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Tag.objects.all().filter(is_active=True)
        project = self.request.query_params.get('project', None)

        if project is not None:
            queryset = queryset.filter(project__id=project)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)


class MapsEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given map and related themes.

    list:
    Return a list of all the existing maps.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = MapSerializer

    def get_queryset(self):
        return Map.objects.all().filter(is_active=True).filter(project__id=self.request.query_params.get('project', None))

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = MapAndThemesSerializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ThemesEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given theme.

    list:
    Return a list of all the existing themes by map.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ThemeSerializer

    def get_queryset(self):
        return Theme.objects.all().filter(is_active=True).filter(visibled=True).filter(map__id=self.request.query_params.get('map', None))


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
