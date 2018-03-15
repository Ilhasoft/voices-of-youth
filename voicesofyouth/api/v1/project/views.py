from rest_framework import permissions, viewsets
from rest_framework.response import Response

from voicesofyouth.project.models import Project
from voicesofyouth.user.models import MapperUser
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
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = Project.objects.all().filter(enabled=True)

        try:
            token = request.META.get('HTTP_AUTHORIZATION').split()[1]
            user = MapperUser.objects.filter(auth_token=token).first()
            queryset = user.projects.all()
        except Exception:
            pass

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
