from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from voicesofyouth.project.models import Project
from voicesofyouth.user.models import MapperUser
from .serializers import ProjectSerializer
from .filters import ProjectFilter


class ProjectsPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = 'page_size'


class ProjectsViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    list:
    Return a list of projects.

    You can use the querystring to get the translated version of the project. E.g. to get a project in portuguese
    brazilian just use: ?lang=pt-br. If the requested translation does not exists you will receive the default language.

    retrieve:
    Return a specific project.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().filter(enabled=True)
    pagination_class = ProjectsPagination
    filter_class = ProjectFilter

    def list(self, request, *args, **kwargs):
        order = self.request.query_params.get('order')
        queryset = self.filter_queryset(self.get_queryset())

        if order:
            queryset = queryset.order_by('-created_on')

        try:
            token = request.META.get('HTTP_AUTHORIZATION').split()[1]
            user = MapperUser.objects.filter(auth_token=token).first()
            queryset = user.projects.all()
        except Exception:
            pass

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
