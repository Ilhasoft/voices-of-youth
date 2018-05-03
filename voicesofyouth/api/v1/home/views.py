from rest_framework import permissions, viewsets
from rest_framework.response import Response

from voicesofyouth.voyhome.models import Slide
from .serializers import HomeSlideSerializer


class HomeSlideEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of images.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = HomeSlideSerializer
    queryset = Slide.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = HomeSlideSerializer(queryset, many=True)
        return Response(serializer.data)
