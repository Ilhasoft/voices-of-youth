from django.conf.urls import url

from voicesofyouth.user.view import AdminView
from voicesofyouth.user.view import MapperDetailView
from voicesofyouth.user.view import MappersListView

urlpatterns = [
    url(r'^admins/$', AdminView.as_view(), name='admin'),
    url(r'^mappers/(?P<mapper_id>[0-9]+)/$', MapperDetailView.as_view(), name='mapper_detail'),
    url(r'^mappers/$', MappersListView.as_view(), name='mappers_list'),
]
