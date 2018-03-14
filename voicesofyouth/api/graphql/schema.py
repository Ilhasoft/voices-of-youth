import graphene
from graphene_django.debug import DjangoDebug
from graphene_django.rest_framework.mutation import SerializerMutation
from voicesofyouth.api.v1.project.serializers import ProjectSerializer

from voicesofyouth.project import schema as project_schema
from voicesofyouth.theme import schema as theme_schema


class Query(project_schema.Query,
            theme_schema.Query,
            graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(SerializerMutation):
    class Meta:
        serializer_class = ProjectSerializer


schema = graphene.Schema(query=Query, mutation=Mutation)
