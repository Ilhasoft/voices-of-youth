from rest_framework import serializers

from voicesofyouth.user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'language', 'avatar', 'username', 'is_mapper')
