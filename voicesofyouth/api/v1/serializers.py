from django.shortcuts import reverse
from rest_framework import serializers

from voicesofyouth.maps.models import Map
from voicesofyouth.report.models import Report
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportMedia
from voicesofyouth.tag.models import Tag
from voicesofyouth.theme.models import Theme
from voicesofyouth.users.models import User


class VoySerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'display_name', 'language', 'user_image', 'personal_url')


class TagSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()

    class Meta:
        model = Tag
        fields = ('id', 'tag', 'urgency_score')


class MapSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='projects-detail'
    )
    # themes = serializers.SerializerMethodField()

    class Meta:
        model = Map
        fields = ('id', 'name', 'bounds', 'is_active', 'project')

    def get_themes(self, obj):
        request = self.context.get('request')
        return '{}{}/?project={}'.format(request.build_absolute_uri(reverse('maps-list')), obj.id, obj.project.id)


class MapAndThemesSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='projects-detail'
    )
    themes = serializers.SerializerMethodField()

    class Meta:
        model = Map
        fields = ('id', 'name', 'bounds', 'is_active', 'project', 'themes')

    def get_themes(self, obj):
        return ThemeSerializer(obj.get_themes(), many=True).data


class ReportMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportMedia
        fields = ('id', 'title', 'description', 'media_type', 'url', 'file', 'screenshot', 'extra', 'language')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComment
        fields = ('id', 'body', 'report')


class ReportCommentsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ReportComment
        fields = ('id', 'body', 'created_on', 'created_by')


class ReportAndMediasSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    all_comments = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ('id', 'project', 'map', 'theme', 'location', 'sharing', 'comments', 'editable',
                  'visibled', 'status', 'images', 'links', 'videos', 'languages', 'tags',
                  'created_on', 'created_by', 'all_comments')

    def get_images(self, obj):
        return ReportMediaSerializer(obj.get_medias(media_type='image'), many=True).data

    def get_links(self, obj):
        return ReportMediaSerializer(obj.get_medias(media_type='link'), many=True).data

    def get_videos(self, obj):
        return ReportMediaSerializer(obj.get_medias(media_type='video'), many=True).data

    def get_languages(self, obj):
        return ReportLanguageSerializer(obj.get_languages(), many=True).data

    def get_tags(self, obj):
        return TagSerializer(obj.get_tags(), many=True).data

    def get_all_comments(self, obj):
        return ReportCommentsSerializer(obj.get_comments(), many=True).data


class ThemeAndReportsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    languages = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reports = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = ('id', 'name', 'project', 'visible', 'languages', 'tags', 'reports')

    def get_languages(self, obj):
        return ThemeTranslationSerializer(obj.get_languages(), many=True).data

    def get_tags(self, obj):
        return TagSerializer(obj.get_tags(), many=True).data

    def get_reports(self, obj):
        return ReportSerializer(obj.get_reports(10), many=True).data
