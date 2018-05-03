from rest_framework import serializers

from voicesofyouth.api.v1.serializers import VoySerializer
from voicesofyouth.voyhome.models import Slide


class HomeSlideSerializer(VoySerializer):
    image = serializers.FileField()

    class Meta:
        model = Slide
        fields = ('image', )
