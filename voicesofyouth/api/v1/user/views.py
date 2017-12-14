from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from voicesofyouth.api.v1.user.serializers import UserSerializer
from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import User


class UsersEndPoint(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer

    def get_queryset(self):
        token = self.request.query_params.get('auth_token')
        theme = self.request.query_params.get('theme')
        user = self.request.user

        if not isinstance(user, AnonymousUser):
            if user.is_admin:
                if theme:
                    theme = get_object_or_404(Theme, id=theme)
                    return theme.mappers_group.user_set.all()
                else:
                    return User.objects.all()
        if token:
            return User.objects.filter(auth_token=token)
