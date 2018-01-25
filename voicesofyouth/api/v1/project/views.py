from rest_framework import permissions, viewsets

from voicesofyouth.project.models import Project
from .serializers import ProjectSerializer


class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of projects.

    You can use the querystring to get the translated version of the project. E.g. to get a project in portuguese
    brazilian just use: ?lang=pt-br. If the requested translation does not exists you will receive the default language.

    retrieve:
    Return a specific project.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Project.objects.all().filter(enabled=True)
    serializer_class = ProjectSerializer
