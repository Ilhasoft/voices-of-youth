from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from voicesofyouth.user.models import User
from voicesofyouth.api.v1.user.serializers import UserSerializer


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
