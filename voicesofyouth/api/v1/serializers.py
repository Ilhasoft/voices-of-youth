from django.shortcuts import reverse
from rest_framework import serializers
# from voicesofyouth.maps.models import Map

from voicesofyouth.tag.models import Tag
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
