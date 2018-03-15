import graphene
from graphene import relay, ObjectType

from django.contrib.gis.db.models.fields import PolygonField
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.converter import convert_django_field
from graphene_django.rest_framework.mutation import SerializerMutation
from taggit.managers import TaggableManager

from voicesofyouth.api.v1.project.serializers import ProjectSerializer
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
        filter_fields = {
            'name': ['exact', 'icontains', 'startswith', 'istartswith'],
            'themes': ['exact', ]
            }
        interfaces = (relay.Node, )


class ProjectQuery(object):
    all_projects = DjangoFilterConnectionField(ProjectNode)
    project = relay.Node.Field(ProjectNode)


class ProjectMutation(SerializerMutation):
    class Meta:
        serializer_class = ProjectSerializer

    # @classmethod
    # def mutate_and_get_payload(cls, input, context, **kwargs):
    #     print(input)
    #     print('-' * 80)
    #     print(context)
    #     print('-' * 80)
    #     print(kwargs)
    #     return super(SerializerMutation, cls).mutate_and_get_payload(input, context, **kwargs)
