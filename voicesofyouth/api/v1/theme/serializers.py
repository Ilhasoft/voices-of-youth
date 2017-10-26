from rest_framework import serializers

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.theme.models import Theme


class ThemeSerializer(VoySerializer):
    tags = serializers.StringRelatedField(
        read_only=True,
        many=True
    )
    project = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='projects-detail'
    )

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
            'reports_count',
            'created_on'
        )
