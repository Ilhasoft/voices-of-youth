from django.conf import settings
from rest_framework import serializers

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.theme.models import Theme
from voicesofyouth.translation.models import Translation


class ThemeSerializer(VoySerializer):
    tags = serializers.StringRelatedField(
        read_only=True,
        many=True
    )
    project = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='voy-api:projects-detail'
    )
    name = serializers.SerializerMethodField()
    pin = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = (
            'id',
            'project',
            'bounds',
            'name',
            'description',
            'tags',
            'color',
            'pin',
            'reports_count',
            'created_on',
            'allow_links',
        )

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

    def get_pin(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(f'{settings.PIN_URL}{obj.color}.png')
