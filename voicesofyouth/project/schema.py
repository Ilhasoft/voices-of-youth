import graphene

from django.contrib.gis.db.models.fields import PolygonField
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field
from taggit.managers import TaggableManager

from voicesofyouth.project.models import Project


@convert_django_field.register(PolygonField)
def polygon_to_graphene(field, registry=None):
    # print(field)
    return graphene.JSONString()

@convert_django_field.register(TaggableManager)
def tags_to_graphene(field, registry=None):
    # print(dir(field))
    return graphene.String()


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project


class Query():
    all_projects = graphene.List(ProjectType)

    def resolve_all_projects(self, info, **kwargs):
        return Project.objects.all()