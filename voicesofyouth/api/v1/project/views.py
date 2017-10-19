from rest_framework import viewsets
from rest_framework import permissions

from voicesofyouth.projects.models import Project
from voicesofyouth.projects.models import ProjectRegion
from .serializers import ProjectSerializer
from .serializers import ProjectRegionSerializer


class ProjectsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectsRegionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ProjectRegion.objects.all()
    serializer_class = ProjectRegionSerializer
