from django.conf.urls import url

from voicesofyouth.voyhome.view import SlideView
from voicesofyouth.voyhome.view import AddSlideView
from voicesofyouth.voyhome.view import RemoveSlideView
from voicesofyouth.voyhome.view import AboutView


urlpatterns = [
    url(r'^slide/$', SlideView.as_view(), name='index_slide'),
    url(r'^slide/new$', AddSlideView.as_view(), name='new_slide'),
    url(r'^slide/(?P<image>[0-9]+)', RemoveSlideView.as_view(), name='remove_slide'),
    url(r'^about/$', AboutView.as_view(), name='index_about'),
]
