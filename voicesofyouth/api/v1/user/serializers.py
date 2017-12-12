from rest_framework import serializers

from voicesofyouth.user.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'language',
            'avatar',
            'username',
            'is_mapper',
            'is_admin'
        )

    def get_avatar(self,
                   obj):
        request = self.context['request']
        return request.build_absolute_uri(obj.get_avatar_display())
