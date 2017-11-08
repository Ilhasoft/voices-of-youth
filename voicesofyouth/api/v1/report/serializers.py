from rest_framework import serializers

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.api.v1.user.serializers import UserSerializer
from voicesofyouth.report.models import Report
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile
from voicesofyouth.report.models import ReportURL
from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import User


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


class ReportURLsSerializer(VoySerializer):
    class Meta:
        model = ReportURL
        fields = (
            'url',
            'report',
        )


class ReportSerializer(VoySerializer):
    tags = serializers.SerializerMethodField()
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=True)
    last_image = ReportFilesSerializer(required=False, read_only=True)
    created_by = UserSerializer(read_only=True)
    can_receive_comments = serializers.BooleanField(read_only=True)
    editable = serializers.BooleanField(read_only=True)
    visible = serializers.BooleanField(read_only=True)
    urls = serializers.StringRelatedField(many=True)

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
            'last_image',
            'urls'
        )

    def get_tags(self, obj):
        return obj.tags.names()


class ReportCommentsSerializer(VoySerializer):
    created_by = UserSerializer(required=False)
    report = serializers.PrimaryKeyRelatedField(queryset=Report.objects.all(), required=True)

    class Meta:
        model = ReportComment
        fields = (
            'id',
            'text',
            'created_by',
            'created_on',
            'modified_on',
            'report'
        )

    def get_author(self, obj):
        return UserSerializer(obj.created_by, context={'request': self.context.get('request')}).data

    def create(self, validated_data):
        """
        We need to ensure the created_by and modified_by never receive AnonymousUser instance. Otherwise we receive
        an exception.
        """
        request = self.context['request']
        if request.user.is_anonymous:
            guest = User.objects.get(username='guest')
            validated_data['created_by'] = guest
            validated_data['modified_by'] = guest
        else:
            validated_data['created_by'] = request.user
            validated_data['modified_by'] = request.user
        return ReportComment.objects.create(**validated_data)


class ReportMediasSerializer(VoySerializer):
    urls = ReportURLsSerializer(many=True)
    files = ReportFilesSerializer(many=True)

    class Meta:
        model = Report
        fields = ('urls', 'files')
