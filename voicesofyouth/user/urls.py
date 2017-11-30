from django.conf.urls import url

from voicesofyouth.user.view import AdminListView, AdminDetailView
from voicesofyouth.user.view import MapperDetailView
from voicesofyouth.user.view import MappersListView

urlpatterns = [
    url(r'^admins/$', AdminListView.as_view(), name='admins_list'),
    url(r'^admins/(?P<admin_id>[0-9]+)/$', AdminDetailView.as_view(), name='admin_detail'),
    url(r'^mappers/(?P<mapper_id>[0-9]+)/$', MapperDetailView.as_view(), name='mapper_detail'),
    url(r'^mappers/$', MappersListView.as_view(), name='mappers_list'),
]
