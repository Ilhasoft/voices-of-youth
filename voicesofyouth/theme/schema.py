import graphene
from graphene import relay, ObjectType, AbstractType

from django.contrib.gis.db.models.fields import PolygonField
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.filter import DjangoFilterConnectionField

from taggit.managers import TaggableManager

from voicesofyouth.theme.models import Theme


@convert_django_field.register(PolygonField)
def polygon_to_graphene(field, registry=None):
    return graphene.JSONString()

@convert_django_field.register(TaggableManager)
def tags_to_graphene(field, registry=None):
    return graphene.String()


class ThemeNode(DjangoObjectType):
    class Meta:
        model = Theme
        filter_fields = ['name', 'project']
        interfaces = (relay.Node, )


class Query(AbstractType):
    all_themes = DjangoFilterConnectionField(ThemeNode)
    theme = relay.Node.Field(ThemeNode)
