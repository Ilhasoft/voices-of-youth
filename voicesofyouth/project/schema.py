import graphene
from graphene import relay, ObjectType

from django.contrib.gis.db.models.fields import PolygonField
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.converter import convert_django_field
from taggit.managers import TaggableManager

from voicesofyouth.project.models import Project


@convert_django_field.register(PolygonField)
def polygon_to_graphene(field, registry=None):
    return graphene.JSONString()

@convert_django_field.register(TaggableManager)
def tags_to_graphene(field, registry=None):
    return graphene.String()


class ProjectNode(DjangoObjectType):
    class Meta:
        model = Project
        filter_fields = ['name', 'themes']
        interfaces = (relay.Node, )


class Query(object):
    all_projects = DjangoFilterConnectionField(ProjectNode)
    project = relay.Node.Field(ProjectNode)
