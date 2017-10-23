from rest_framework import permissions
from rest_framework import viewsets

from voicesofyouth.project.models import Project
from voicesofyouth.project.models import ProjectRegion
from voicesofyouth.project.models import ProjectTranslation
from .serializers import ProjectRegionSerializer
from .serializers import ProjectSerializer
from .serializers import ProjectTranslationSerializer


class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectsRegionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = ProjectRegion.objects.all()
    serializer_class = ProjectRegionSerializer


class ProjectsTranslationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = ProjectTranslation.objects.all()
    serializer_class = ProjectTranslationSerializer
