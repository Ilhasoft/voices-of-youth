from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.project.models import Project


class ProjectSerializer(VoySerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'path', 'language', 'boundary', 'thumbnail', 'window_title')
