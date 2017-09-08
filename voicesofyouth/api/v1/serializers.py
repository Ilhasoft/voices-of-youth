from rest_framework import serializers
from voicesofyouth.projects.models import Project
from voicesofyouth.tags.models import Tag
from voicesofyouth.maps.models import Map
from voicesofyouth.themes.models import Theme, ThemeLanguage
from voicesofyouth.users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'display_name', 'language', 'user_image', 'personal_url')


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'path', 'is_active', 'language')


class TagSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer(read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'system_tag', 'urgency_score', 'is_active', 'project')


class MapSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Map
        fields = ('id', 'name', 'bounds', 'is_active', 'project')


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

    class Meta:
        model = Theme
        fields = ('id', 'name', 'project', 'visibled', 'cover', 'created_by', 'created_on', 'modified_on', 'languages')

    def get_languages(self, obj):
        return ThemeLanguageSerializer(obj.get_languages(), many=True).data
