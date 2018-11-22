from django.conf.urls import url

from voicesofyouth.voyhome.view import SlideView
from voicesofyouth.voyhome.view import AddSlideView
from voicesofyouth.voyhome.view import RemoveSlideView
from voicesofyouth.voyhome.view import AboutView
from voicesofyouth.voyhome.view import JoinRequestsView
from voicesofyouth.voyhome.view import ApproveRequestsView
from voicesofyouth.voyhome.view import JoinRequestsDetailView
from voicesofyouth.voyhome.view import RemoveRequestsView
from voicesofyouth.voyhome.view import ReorderSlideView


urlpatterns = [
    url(r'^slide/$', SlideView.as_view(), name='index_slide'),
    url(r'^slide/new$', AddSlideView.as_view(), name='new_slide'),
    url(r'^slide/(?P<image>[0-9]+)/remove$', RemoveSlideView.as_view(), name='remove_slide'),
    url(r'^slide/(?P<image>[0-9]+)/(?P<act>[\w]+)$', ReorderSlideView.as_view(), name='reorder_slide'),
    url(r'^about/$', AboutView.as_view(), name='index_about'),
    url(r'^requests/$', JoinRequestsView.as_view(), name='index_requests'),
    url(r'^requests/detail/(?P<mapper>[0-9]+)', JoinRequestsDetailView.as_view(), name='requests_view'),
    url(r'^requests/approve/(?P<mapper>[0-9]+)', ApproveRequestsView.as_view(), name='requests_approve'),
    url(r'^requests/remove/(?P<mapper>[0-9]+)', RemoveRequestsView.as_view(), name='requests_remove'),
]
