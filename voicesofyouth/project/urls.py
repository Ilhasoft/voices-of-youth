from django.conf.urls import url

from voicesofyouth.project.view import AddProjectView
from voicesofyouth.project.view import ProjectView

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='index'),
    url(r'^new/', AddProjectView.as_view(), name='new'),
]
