import graphene

from voicesofyouth.project import schema as project_schema
from voicesofyouth.theme import schema as theme_schema


class Query(project_schema.Query,
            theme_schema.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
