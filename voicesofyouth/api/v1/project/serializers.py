from django.conf import settings
from rest_framework import serializers
from easy_thumbnails.files import get_thumbnailer

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.project.models import Project
from voicesofyouth.translation.models import Translation


class ProjectSerializer(VoySerializer):
    languages = serializers.SerializerMethodField()
    years = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    thumbnail_cropped = serializers.FileField()
    thumbnail_home_responsive = serializers.SerializerMethodField()
    thumbnail_home = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'path',
            'language',
            'bounds',
            'thumbnail',
            'window_title',
            'languages',
            'years',
            'thumbnail_cropped',
            'thumbnail_home_responsive',
            'thumbnail_home',
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

    def get_thumbnail_home_responsive(self, obj):
        if obj.thumbnail:
            request = self.context['request']
            return request.build_absolute_uri(get_thumbnailer(obj.thumbnail)['project_thumbnail_home_responsive_cropped'].url)
        return ""

    def get_thumbnail_home(self, obj):
        if obj.thumbnail:
            request = self.context['request']
            return request.build_absolute_uri(get_thumbnailer(obj.thumbnail)['project_thumbnail_home_cropped'].url)
        return ""
