from rest_framework import serializers

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.api.v1.user.serializers import UserSerializer
from voicesofyouth.report.models import FILE_TYPE_IMAGE
from voicesofyouth.report.models import Report
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile
from voicesofyouth.report.models import ReportURL



class PointField(serializers.Field):
    def to_representation(self, value):
        return value.coords


class ReportFilesSerializer(VoySerializer):
    class Meta:
        model = ReportFile
        fields = (
            'title',
            'description',
            'media_type',
            'file',
        )


class ReportSerializer(VoySerializer):
    tags = serializers.StringRelatedField(
        read_only=True,
        many=True
    )
    theme_id = serializers.PrimaryKeyRelatedField(read_only=True)
    location = PointField()
    theme_color = serializers.SerializerMethodField()
    last_image = ReportFilesSerializer()
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
            'author',
            'last_image'
        )

    def get_theme_color(self, obj):
        return obj.theme.color


class ReportCommentsSerializer(VoySerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = ReportComment
        fields = (
            'id',
            'text',
            'author',
            'created_on',
            'modified_on'
        )

    def get_author(self, obj):
        return UserSerializer(obj.created_by).data


class ReportURLsSerializer(VoySerializer):
    class Meta:
        model = ReportURL
        fields = (
            'url',
        )


class ReportMediasSerializer(VoySerializer):
    urls = ReportURLsSerializer(many=True)
    files = ReportFilesSerializer(many=True)

    class Meta:
        model = Report
        fields = ('urls', 'files')
