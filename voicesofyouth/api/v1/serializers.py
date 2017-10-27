from rest_framework import serializers

from voicesofyouth.user.models import User


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
        fields = ('id', 'first_name', 'last_name', 'language', 'avatar', 'username')
