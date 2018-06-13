from rest_framework import permissions, viewsets, mixins
from rest_framework import status
from rest_framework.response import Response

from voicesofyouth.voyhome.models import Slide
from voicesofyouth.voyhome.models import About
from voicesofyouth.user.models import VoyUser
from .serializers import HomeSlideSerializer
from .serializers import HomeAboutSerializer
from .serializers import HomeContactSerializer


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


class HomeContactEndPoint(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    """
    create:
    Create a new contact message.
    """
    permission_classes = [permissions.AllowAny, ]
    serializer_class = HomeContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(instance)
        return Response(instance, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = VoyUser.objects.get(username='guest')
        serializer.save(created_by=user, modified_by=user)
