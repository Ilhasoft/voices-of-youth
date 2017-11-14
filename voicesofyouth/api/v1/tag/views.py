from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from voicesofyouth.api.v1.tag.serializers import TagSerializer
from voicesofyouth.project.models import Project
from voicesofyouth.tag.models import Tag
from voicesofyouth.theme.models import Theme


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return tags related with the theme or project.

    User cannot create tags directly via API. Only super admins or local admins can do that.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.prefetch_related('taggit_taggeditem_items__tag').all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        """
        You can filter tags by project or by theme. If you make a request with project and theme at same time, the
        response will include all tags from the project and the theme.

        If you inform a theme that not belong to project, you will receive a 404.
        """
        url_query = self.request.query_params
        theme_id = url_query.get('theme', 0)
        project_id = url_query.get('project', 0)
        ct_project = ContentType.objects.get_for_model(Project)
        ct_theme = ContentType.objects.get_for_model(Theme)
        qs_tags = []

        if theme_id and project_id:
            # If user inform project and theme, its needs to belong to project. Otherwise we return 404.
            try:
                project = Project.objects.get(id=project_id)
                if project:
                    project.themes.get(id=theme_id)
            except (Project.DoesNotExist, Theme.DoesNotExist):
                return Response(status=status.HTTP_404_NOT_FOUND)

            qs_tags = self.queryset.filter(Q(taggit_taggeditem_items__content_type=ct_theme,
                                             taggit_taggeditem_items__object_id=theme_id) |
                                           Q(taggit_taggeditem_items__content_type=ct_project,
                                             taggit_taggeditem_items__object_id=project_id)).distinct()
        elif theme_id:
            qs_tags = self.queryset.filter(Q(taggit_taggeditem_items__content_type=ct_theme,
                                             taggit_taggeditem_items__object_id=theme_id)).distinct()
        elif project_id:
            qs_tags = self.queryset.filter(Q(taggit_taggeditem_items__content_type=ct_project,
                                             taggit_taggeditem_items__object_id=project_id)).distinct()

        if len(qs_tags) > 0:
            return Response(self.serializer_class(qs_tags, many=True).data)
        return Response(status=status.HTTP_404_NOT_FOUND)
