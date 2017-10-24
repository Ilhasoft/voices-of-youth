from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from voicesofyouth.project.models import Project
from voicesofyouth.translation.models import Translation
from .serializers import ProjectSerializer


class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def retrieve(self, request, pk=None):
        lang = self.request.query_params.get('lang', '').strip()
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        Translation.translate_object(project, lang)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
