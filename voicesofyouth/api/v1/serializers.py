from rest_framework import serializers
from voicesofyouth.projects.models import Project
from voicesofyouth.tags.models import Tag


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'path', 'is_active', 'language')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'system_tag', 'urgency_score', 'is_active', 'project')
