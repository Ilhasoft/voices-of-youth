from rest_framework import serializers


class VoySerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        return super().create(validated_data)
