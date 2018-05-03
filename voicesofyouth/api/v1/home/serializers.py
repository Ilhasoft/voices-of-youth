from rest_framework import serializers
from voicesofyouth.voyhome.models import Slide
from voicesofyouth.voyhome.models import About


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
