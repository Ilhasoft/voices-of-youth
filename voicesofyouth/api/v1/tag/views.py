from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from voicesofyouth.api.v1.tag.serializers import TagSerializer
from voicesofyouth.tag.models import Tag
from voicesofyouth.theme.models import Theme


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return tags related with the theme or project.

    User cannot create tags directly via API. Only super admins or local admins can do that.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        """
        You can filter tags by project or by theme. If you make a request with project and theme at same time, only the
        theme will be considered.
        """
        query = {}
        url_query = self.request.query_params
        query['content_type'] = ContentType.objects.get_for_model(Theme)
        if 'theme' in url_query:
            theme_id = url_query.get('theme')
            query['object_id__in'] = [theme.id for theme in Theme.objects.filter(id=theme_id)]
        elif 'project' in url_query:
            project_id = url_query.get('project')
            query['object_id__in'] = [theme.id for theme in Theme.objects.filter(project__id=project_id)]
        qs = self.queryset.filter(**query)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)
