import graphene

from django.contrib.gis.db.models.fields import PolygonField
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field
from taggit.managers import TaggableManager

from voicesofyouth.theme.models import Theme


@convert_django_field.register(PolygonField)
def polygon_to_graphene(field, registry=None):
    # print(field)
    return graphene.JSONString()

@convert_django_field.register(TaggableManager)
def tags_to_graphene(field, registry=None):
    # print(dir(field))
    return graphene.String()


class ThemeType(DjangoObjectType):
    class Meta:
        model = Theme


class Query():
    all_themes = graphene.List(ThemeType)

    def resolve_all_themes(self, info, **kwargs):
        return Theme.objects.all()