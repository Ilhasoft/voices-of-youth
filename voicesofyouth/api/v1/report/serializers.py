from rest_framework import serializers

from voicesofyouth.api.v1.user.serializers import UserSerializer
from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.report.models import Report, ReportComment


class PointField(serializers.Field):
    def to_representation(self, value):
        return value.coords


class ReportSerializer(VoySerializer):
    tags = serializers.StringRelatedField(
        read_only=True,
        many=True
    )
    theme_id = serializers.PrimaryKeyRelatedField(read_only=True)
    location = PointField()
    theme_color = serializers.SerializerMethodField()
    author = UserSerializer()

    class Meta:
        model = Report
        fields = (
            'id',
            'theme_id',
            'location',
            'can_receive_comments',
            'editable',
            'visible',
            'created_on',
            'description',
            'name',
            'tags',
            'theme_color',
            'author'
        )

    def get_theme_color(self, obj):
        return obj.theme.color


class ReportCommentsSerializer(VoySerializer):
    report = serializers.HyperlinkedRelatedField(read_only=True, view_name='reports-detail')
    author = UserSerializer()

    class Meta:
        model = ReportComment
        fields = (
            'id',
            'report',
            'text',
            'author',
        )
