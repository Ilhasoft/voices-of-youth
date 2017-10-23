from rest_framework import serializers

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.project.models import Project
from voicesofyouth.project.models import ProjectTranslation


class ProjectSerializer(VoySerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'path', 'language', 'boundary', 'thumbnail', 'window_title')


class ProjectTranslationSerializer(VoySerializer):
    project = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='projects-detail'
    )

    class Meta:
        model = ProjectTranslation
        fields = ('id', 'language', 'name', 'window_title', 'description')
