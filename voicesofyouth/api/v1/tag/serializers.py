from rest_framework import serializers

from voicesofyouth.tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'tag', 'urgency_score')

    def get_tag(self, obj):
        return obj.name
