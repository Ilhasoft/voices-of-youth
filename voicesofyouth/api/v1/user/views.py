from django.contrib.auth.models import AnonymousUser

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

from voicesofyouth.api.v1.user.serializers import UserSerializer
from voicesofyouth.api.v1.user.serializers import UserChangeSetSerializer
from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import User


class UsersEndPoint(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_queryset(self):
        token = self.request.query_params.get('auth_token')
        theme = self.request.query_params.get('theme')
        user = self.request.user

        if not isinstance(user, AnonymousUser):
            if user.is_admin and not token:
                if theme:
                    theme = get_object_or_404(Theme, id=theme)
                    return theme.mappers_group.user_set.all()
                else:
                    return User.objects.all()
        if token:
            return User.objects.filter(auth_token=token)

    def create(self, request, *args, **kwargs):
        serializer = UserChangeSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.set_password(serializer.data['password'])
        user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    '''def update(self, request, *args, **kwargs):
        print("ATUALIZANDO")
        print(request.META.get('HTTP_AUTHORIZATION'))

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)'''
