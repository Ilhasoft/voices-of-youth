from rest_framework import serializers
from django.conf import settings

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.project.models import Project


class ProjectSerializer(VoySerializer):

    languages = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'path',
            'language',
            'boundary',
            'thumbnail',
            'window_title',
            'languages',
        )

    def get_languages(self, obj):
        return {next(filter(lambda l: t.language in l, settings.LANGUAGES)) for t in obj.translations.all()}
