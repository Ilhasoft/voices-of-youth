from rest_framework import serializers
from voicesofyouth.projects.models import Project
from voicesofyouth.tags.models import Tag
from voicesofyouth.maps.models import Map
from voicesofyouth.themes.models import Theme


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'path', 'is_active', 'language')


class TagSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer(read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'system_tag', 'urgency_score', 'is_active', 'project')


class MapSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Map
        fields = ('id', 'name', 'bounds', 'is_active', 'project')


class ThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = ('id', 'name', 'project', 'visibled', 'cover')
