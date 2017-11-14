from rest_framework import serializers

from voicesofyouth.user.models import User


class MapperSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'username')

    def get_full_name(self, obj):
        return obj.get_full_name()
