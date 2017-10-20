from rest_framework import permissions
from rest_framework import viewsets

from voicesofyouth.projects.models import Project
from voicesofyouth.projects.models import ProjectRegion
from voicesofyouth.projects.models import ProjectTranslation
from .serializers import ProjectRegionSerializer
from .serializers import ProjectSerializer
from .serializers import ProjectTranslationSerializer


class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectsRegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectRegion.objects.all()
    serializer_class = ProjectRegionSerializer


class ProjectsTranslationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectTranslation.objects.all()
    serializer_class = ProjectTranslationSerializer
