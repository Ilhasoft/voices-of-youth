from django.shortcuts import reverse
from rest_framework import serializers
from voicesofyouth.projects.models import Project
from voicesofyouth.tags.models import Tag
from voicesofyouth.maps.models import Map
from voicesofyouth.themes.models import Theme, ThemeLanguage
from voicesofyouth.users.models import User
from voicesofyouth.reports.models import Report, ReportMedias, ReportLanguage, ReportComments


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'display_name', 'language', 'user_image', 'personal_url')


class ProjectSerializer(serializers.ModelSerializer):
    maps = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'path', 'is_active', 'language', 'maps')

    def get_maps(self, obj):
        request = self.context.get('request')
        return '{}?project={}'.format(request.build_absolute_uri(reverse('maps-list')), obj.id)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'system_tag', 'urgency_score', 'is_active')


class MapSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    themes = serializers.SerializerMethodField()

    class Meta:
        model = Map
        fields = ('id', 'name', 'bounds', 'is_active', 'project', 'themes')

    def get_themes(self, obj):
        request = self.context.get('request')
        return '{}{}/?project={}'.format(request.build_absolute_uri(reverse('maps-list')), obj.id, obj.project.id)


class MapAndThemesSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    themes = serializers.SerializerMethodField()

    class Meta:
        model = Map
        fields = ('id', 'name', 'bounds', 'is_active', 'project', 'themes')

    def get_themes(self, obj):
        return ThemeSerializer(obj.get_themes(), many=True).data


class ThemeLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeLanguage
        fields = ('id', 'language', 'title', 'description', 'theme', 'created_on', 'modified_on')


class ThemeSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    languages = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    reports = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = ('id', 'url', 'name', 'project', 'visibled', 'cover', 'created_by', 'created_on', 'modified_on', 'languages', 'tags', 'reports')

    def get_languages(self, obj):
        return ThemeLanguageSerializer(obj.get_languages(), many=True).data

    def get_tags(self, obj):
        return TagSerializer(obj.get_tags(), many=True).data

    def get_url(self, obj):
        return reverse('themes-detail', kwargs={'pk': obj.id})

    def get_reports(self, obj):
        return obj.get_total_reports()


class ReportMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportMedias
        fields = ('id', 'title', 'description', 'media_type', 'url', 'file', 'screenshot', 'extra', 'language')


class ReportLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportLanguage
        fields = ('id', 'language', 'title', 'description', 'created_on', 'modified_on')


class ReportSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ('id', 'url', 'project', 'map', 'theme', 'location', 'sharing', 'comments', 'editable', 'visibled', 'status', 'image', 'created_on')

    def get_url(self, obj):
        return reverse('reports-detail', kwargs={'pk': obj.id})

    def get_image(self, obj):
        images = obj.get_medias(media_type='image')

        if len(images) > 0:
            return ReportMediaSerializer(images[0]).data

        return None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComments
        fields = ('id', 'body', 'report')


class ReportCommentsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ReportComments
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
        fields = ('id', 'project', 'map', 'theme', 'location', 'sharing', 'comments', 'editable', 'visibled', 'status', 'images', 'links', 'videos', 'languages', 'tags', 'created_on', 'created_by', 'all_comments')

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
        fields = ('id', 'name', 'project', 'visibled', 'cover', 'created_by', 'created_on', 'modified_on', 'languages', 'tags', 'reports')

    def get_languages(self, obj):
        return ThemeLanguageSerializer(obj.get_languages(), many=True).data

    def get_tags(self, obj):
        return TagSerializer(obj.get_tags(), many=True).data

    def get_reports(self, obj):
        return ReportSerializer(obj.get_reports(10), many=True).data
