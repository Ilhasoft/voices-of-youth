from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from voicesofyouth.api.v1.serializers import TagSerializer
from voicesofyouth.tag.models import Tag
from voicesofyouth.theme.models import Theme
from voicesofyouth.users.models import User
from .serializers import UserSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Only list tags related with theme.

    User cannot create tags directly via API because tags cannot exists without related data. e.g. When create new
    Theme, if user send a list of tags(comma separated) the system will created these tags automatically.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TagSerializer

    def get_queryset(self):
        theme = get_object_or_404(Theme, pk=self.request.query_params.get('theme', 0))
        return Tag.objects.filter(object_id=theme.id)


class UsersEndPoint(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given theme.

    list:
    Return a list of all the existing themes by map.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all().filter(is_active=True)
