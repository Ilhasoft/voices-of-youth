from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from voicesofyouth.user.models import User


class VoySerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        mapper_id = request.data.get('mapper_id')
        if mapper_id and user.is_admin:
            mapper = get_object_or_404(User, id=mapper_id)
            validated_data['created_by'] = mapper
            validated_data['modified_by'] = mapper
        else:
            validated_data['created_by'] = user
            validated_data['modified_by'] = user
        return super().create(validated_data)
