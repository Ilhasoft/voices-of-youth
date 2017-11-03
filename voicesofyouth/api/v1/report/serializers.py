from rest_framework import serializers

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.api.v1.user.serializers import UserSerializer
from voicesofyouth.report.models import FILE_TYPE_IMAGE
from voicesofyouth.report.models import Report
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile
from voicesofyouth.report.models import ReportURL

from voicesofyouth.theme.models import Theme


class ReportFilesSerializer(VoySerializer):
    created_by = UserSerializer()

    class Meta:
        model = ReportFile
        fields = (
            'title',
            'description',
            'media_type',
            'file',
            'created_by',
        )


class ReportSerializer(VoySerializer):
    tags = serializers.StringRelatedField(
        read_only=True,
        many=True
    )
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=True)
    last_image = ReportFilesSerializer(required=False, read_only=True)
    created_by = UserSerializer(read_only=True)
    can_receive_comments = serializers.BooleanField(read_only=True)
    editable = serializers.BooleanField(read_only=True)
    visible = serializers.BooleanField(read_only=True)

    class Meta:
        model = Report
        fields = (
            'id',
            'theme',
            'location',
            'can_receive_comments',
            'editable',
            'visible',
            'created_on',
            'description',
            'name',
            'tags',
            'theme_color',
            'created_by',
            'last_image'
        )


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
        return UserSerializer(obj.created_by, context={'request': self.context.get('request')}).data


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
