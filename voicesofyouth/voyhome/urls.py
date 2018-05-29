from django.conf.urls import url

from voicesofyouth.voyhome.view import SlideView
from voicesofyouth.voyhome.view import AddSlideView
from voicesofyouth.voyhome.view import RemoveSlideView
from voicesofyouth.voyhome.view import AboutView
from voicesofyouth.voyhome.view import ContactView
from voicesofyouth.voyhome.view import ContactMessageView
from voicesofyouth.voyhome.view import ReorderSlideView


urlpatterns = [
    url(r'^slide/$', SlideView.as_view(), name='index_slide'),
    url(r'^slide/new$', AddSlideView.as_view(), name='new_slide'),
    url(r'^slide/(?P<image>[0-9]+)/remove$', RemoveSlideView.as_view(), name='remove_slide'),
    url(r'^slide/(?P<image>[0-9]+)/(?P<act>[\w]+)$', ReorderSlideView.as_view(), name='reorder_slide'),
    url(r'^about/$', AboutView.as_view(), name='index_about'),
    url(r'^contact/$', ContactView.as_view(), name='index_contact'),
    url(r'^contact/message/(?P<contact>[0-9]+)', ContactMessageView.as_view(), name='message_view'),
]
