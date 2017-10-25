from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from voicesofyouth.project.models import Project
from voicesofyouth.translation.models import Translation
from .serializers import ProjectSerializer


class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    You can use querystring to translate the project. E.g.: /api/projects/1/?lang=pt-br
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def retrieve(self, request, pk=None):
        lang = self.request.query_params.get('lang', '').strip()
        project = get_object_or_404(self.queryset, pk=pk)
        Translation.objects.translate_object(project, lang)
        serializer = self.serializer_class(project)
        return Response(serializer.data)
