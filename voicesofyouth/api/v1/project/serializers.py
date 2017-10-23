from rest_framework import serializers

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.project.models import Project
from voicesofyouth.project.models import ProjectRegion


class ProjectSerializer(VoySerializer):
    project_region = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='projects-regions-detail'
    )

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'path', 'language', 'project_region', 'thumbnail', 'window_title')


class ProjectRegionSerializer(VoySerializer):
    project = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='projects-detail'
    )

    class Meta:
        model = ProjectRegion
        fields = ('id', 'project', 'region')


class ProjectTranslationSerializer(VoySerializer):
    project = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='projects-detail'
    )

    class Meta:
        model = ProjectRegion
        fields = ('id', 'project', 'region')
