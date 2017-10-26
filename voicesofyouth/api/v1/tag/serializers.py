from rest_framework import serializers

from voicesofyouth.tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()

    class Meta:
        model = Tag
        fields = ('id', 'tag', 'urgency_score')
