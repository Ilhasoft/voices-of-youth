from django.conf.urls import url

from graphene_django.views import GraphQLView
from voicesofyouth.api.graphql.schema import schema

from .v1.urls import urlpatterns


urlpatterns.append(url(r'^graphql/', GraphQLView.as_view(graphiql=True, schema=schema)))
