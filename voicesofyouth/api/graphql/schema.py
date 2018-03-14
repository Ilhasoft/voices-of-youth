import graphene
from graphene_django.debug import DjangoDebug
from voicesofyouth.api.v1.theme.serializers import ThemeSerializer

from voicesofyouth.project.schema import ProjectQuery
from voicesofyouth.project.schema import ProjectMutation
from voicesofyouth.theme.schema import ThemeQuery
from voicesofyouth.theme.schema import ThemeMutation


class Query(ProjectQuery,
            ThemeQuery,
            graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutations(graphene.ObjectType):
    """
    Here you can find all mutations implemented on VoY.
    """
    project = ProjectMutation.Field()
    theme = ThemeMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
