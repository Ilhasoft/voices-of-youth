import graphene
from graphene import relay, ObjectType

from django.contrib.gis.db.models.fields import PolygonField
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from taggit.managers import TaggableManager

from voicesofyouth.theme.models import Theme
from voicesofyouth.api.v1.theme.serializers import ThemeSerializer


@convert_django_field.register(PolygonField)
def polygon_to_graphene(field, registry=None):
    return graphene.JSONString()


@convert_django_field.register(TaggableManager)
def tags_to_graphene(field, registry=None):
    return graphene.String()


class ThemeNode(DjangoObjectType):
    """
    Theme node.
    """
    class Meta:
        model = Theme
        filter_fields = {
            'id': ['exact', ],
            'name': ['exact', 'icontains', 'istartswith'],
            'project': ['exact', ]
        }
        interfaces = (relay.Node, )


class ThemeQuery(object):
    """
    Theme query.
    """
    all_themes = DjangoFilterConnectionField(ThemeNode)
    theme = relay.Node.Field(ThemeNode)


class ThemeMutation(SerializerMutation):
    """
    Theme mutation.
    """
    class Meta:
        serializer_class = ThemeSerializer
