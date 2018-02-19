from rest_framework import serializers

from voicesofyouth.user.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'language',
            'avatar',
            'email',
            'username',
            'is_mapper',
            'is_admin'
        )

    def get_avatar(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(obj.get_avatar_display())


class UserChangeSetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'avatar',
            'first_name',
            'username',
            'email',
            'password',
        )

    def validate(self, data):
        user = User.objects.get(username=data['username'])
        if user is not None:
            raise serializers.ValidationError('Username already exists.')

        return data
