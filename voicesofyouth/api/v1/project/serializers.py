from django.conf import settings
from rest_framework import serializers

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.project.models import Project
from voicesofyouth.translation.models import Translation


class ProjectSerializer(VoySerializer):
    languages = serializers.SerializerMethodField()
    years = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

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
            'years'
        )

    def get_languages(self, obj):
        return {next(filter(lambda l: t.language in l, settings.LANGUAGES)) for t in obj.translations.all()}

    def get_years(self, obj):
        return Project.objects.dates('created_on', 'year')

    def get_name(self, obj):
        request = self.context['request']
        lang_code = request.query_params.get('lang', '').strip()
        Translation.objects.translate_object(obj, lang_code=lang_code)
        return obj.name

    def get_description(self, obj):
        request = self.context['request']
        lang_code = request.query_params.get('lang', '').strip()
        Translation.objects.translate_object(obj, lang_code=lang_code)
        return obj.description
