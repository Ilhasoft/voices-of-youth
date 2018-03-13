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
    project = graphene.Field(ProjectType,
                             id=graphene.Int(),
                             name=graphene.String())

    def resolve_all_projects(self, info, **kwargs):
        return Project.objects.all()

    def resolve_project(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Project.objects.get(pk=id)

        if name is not None:
            return Project.objects.get(name=name)
        
        return None
