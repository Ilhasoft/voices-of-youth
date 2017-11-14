from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from voicesofyouth.api.v1.mapper.filters import MapperUserFilter
from voicesofyouth.api.v1.mapper.serializers import MapperSerializer
from voicesofyouth.user.models import MapperUser


class MappersEndPoint(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = MapperSerializer
    queryset = MapperUser.objects.all()
    filter_class = MapperUserFilter
