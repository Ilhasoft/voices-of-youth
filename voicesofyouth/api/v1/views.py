from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from voicesofyouth.tags.models import Tag
from voicesofyouth.projects.models import Project

from .serializers import TagSerializer, ProjectSerializer


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
