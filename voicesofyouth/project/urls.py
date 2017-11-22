from django.conf.urls import url

from voicesofyouth.project.view import AddProjectView
from voicesofyouth.project.view import ProjectView
from voicesofyouth.project.view import EditProjectView

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='index'),
    url(r'^new/', AddProjectView.as_view(), name='new'),
    url(r'^(?P<project>[0-9]+)/edit$', EditProjectView.as_view(), name='edit'),
]
