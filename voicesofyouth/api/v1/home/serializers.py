import requests
import datetime
import pytz

from rest_framework import serializers
from voicesofyouth.voyhome.models import Slide
from voicesofyouth.voyhome.models import About
from voicesofyouth.user.models import MapperUser
from voicesofyouth.project.models import Project
from voicesofyouth.settings import RECAPTCHA_SECRET_KEY


class HomeSlideSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Slide
        fields = ('thumbnail', )

    def get_thumbnail(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(obj.thumbnail_home.url)


class HomeAboutSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = About
        fields = (
            'thumbnail',
            'about_project',
            'about_voy',
        )

    def get_thumbnail(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(obj.thumbnail.url)


class HomeContactSerializer(serializers.ModelSerializer):
    captcha = serializers.CharField()
    password = serializers.CharField()
    accepted = serializers.IntegerField()
    project = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = MapperUser
        fields = (
            'captcha',
            'name',
            'username',
            'password',
            'email',
            'country',
            'age',
            'tell_about',
            'project',
            'accepted',
        )

    def validate_accepted(self, value):
        return pytz.utc.localize(datetime.datetime.fromtimestamp(value))

    def validate_captcha(self, value):
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': value
        }

        response = requests.post(url, values)
        result = response.json()

        if result['success'] is False:
            raise serializers.ValidationError('Invalid captcha.')

        return value

    def create(self, validated_data):
        validated_data.pop('captcha')
        validated_data.pop('accepted')

        project_id = validated_data.get('project')
        validated_data.pop('project')

        first_name = validated_data.get('name')
        validated_data.pop('name')

        mapper = MapperUser.objects.create(**validated_data)
        mapper.is_active = False
        mapper.set_password(validated_data.get('name'))
        mapper.first_name = first_name
        mapper.save()

        project = Project.objects.get(pk=project_id)
        theme = project.themes.first()
        theme.mappers_group.user_set.add(mapper)

        return mapper
