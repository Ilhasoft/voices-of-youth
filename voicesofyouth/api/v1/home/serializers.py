import requests
import datetime
import pytz

from rest_framework import serializers
from voicesofyouth.voyhome.models import Slide
from voicesofyouth.voyhome.models import About
from voicesofyouth.voyhome.models import Contact
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
    accepted = serializers.IntegerField()

    class Meta:
        model = Contact
        fields = (
            'captcha',
            'name',
            'email',
            'description',
            'want',
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
        return Contact.objects.create(**validated_data)
