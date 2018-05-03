from rest_framework import permissions, viewsets

from voicesofyouth.voyhome.models import Slide
from voicesofyouth.voyhome.models import About

from .serializers import HomeSlideSerializer
from .serializers import HomeAboutSerializer


class HomeSlideEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of images.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = HomeSlideSerializer
    queryset = Slide.objects.all()


class HomeAboutEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of images.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = HomeAboutSerializer
    queryset = About.objects.all()
