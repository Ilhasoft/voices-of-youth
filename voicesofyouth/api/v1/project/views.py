from rest_framework import permissions, viewsets

from voicesofyouth.project.models import Project
from .serializers import ProjectSerializer


class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return a list of projects.

    You can use the querystring to get the translated version of the project. E.g. to get a project in portuguese
    brazilian just use: ?lang=pt-br

    retrieve:
    Return a specific project.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
