from django.conf import settings
from rest_framework import serializers
import magic

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.api.v1.user.serializers import UserSerializer

from voicesofyouth.report.models import Report, FILE_TYPE_IMAGE, FILE_TYPE_VIDEO
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile
from voicesofyouth.report.models import ReportURL
from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import User


class ReportFilesSerializer(VoySerializer):
    id = serializers.IntegerField(read_only=True)
    created_by = UserSerializer(required=False)
    media_type = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    report_id = serializers.IntegerField()
    file = serializers.FileField()

    class Meta:
        model = ReportFile
        fields = (
            'id',
            'title',
            'description',
            'media_type',
            'file',
            'created_by',
            'report_id'
        )

    def create(self, validated_data):
        mime_type = magic.from_buffer(validated_data['file'].read(), mime=True)
        if mime_type.startswith('image'):
            validated_data['media_type'] = FILE_TYPE_IMAGE
        else:
            validated_data['media_type'] = FILE_TYPE_VIDEO
        return ReportFile.objects.create(**validated_data)


class ReportURLsSerializer(VoySerializer):
    class Meta:
        model = ReportURL
        fields = (
            'url',
        )

    def save(self, **kwargs):
        report = kwargs.get('report')
        self.validated_data['report'] = report
        return super(ReportURLsSerializer, self).save(**kwargs)


class ReportSerializer(VoySerializer):
    tags = serializers.SerializerMethodField()
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=True)
    last_image = ReportFilesSerializer(required=False, read_only=True)
    created_by = UserSerializer(read_only=True)
    can_receive_comments = serializers.BooleanField(read_only=True)
    editable = serializers.BooleanField(read_only=True)
    visible = serializers.BooleanField(read_only=True)
    pin = serializers.SerializerMethodField(read_only=True)
    urls = serializers.StringRelatedField(many=True, read_only=True)
    files = ReportFilesSerializer(many=True, read_only=True)

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
            'pin',
            'created_by',
            'last_image',
            'status',
            'urls',
            'files'
        )

    def get_tags(self, obj):
        return obj.tags.names()

    def get_pin(self, obj):
        if hasattr(obj, 'theme'):
            request = self.context['request']
            return request.build_absolute_uri(f'{settings.PIN_URL}{obj.theme.color}.png')

    def save(self, **kwargs):
        report = super(ReportSerializer, self).save()
        report.tags.remove(*report.tags.all())
        report.tags.add(*kwargs.get('tags'))

        if kwargs.get('urls') is not None:
            ReportURL.objects.filter(report=report).delete()
            request = self.context['request']
            for url in kwargs.get('urls'):
                ReportURL.objects.create(
                    url=url,
                    report=report,
                    created_by=request.user,
                    modified_by=request.user
                )

        return report


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
    urls = serializers.StringRelatedField(many=True)
    files = ReportFilesSerializer(many=True)

    class Meta:
        model = Report
        fields = ('urls', 'files')
