from rest_framework import serializers

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.report.models import Report


class ReportSerializer(VoySerializer):
    tags = serializers.StringRelatedField(
        read_only=True,
        many=True
    )
    theme = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='themes-detail'
    )

    class Meta:
        model = Report
        fields = ('id',
                  'theme',
                  'location',
                  'comments',
                  'editable',
                  'visible',
                  'created_on',
                  'description',
                  'name',
                  'tags')
