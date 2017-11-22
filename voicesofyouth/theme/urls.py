from django.conf.urls import url

from voicesofyouth.theme.view import ThemeView
from voicesofyouth.theme.view import AddThemeView
from voicesofyouth.theme.view import EditThemeView

urlpatterns = [
    url(r'^(?P<project>[0-9]+)/$', ThemeView.as_view(), name='index'),
    url(r'^(?P<project>[0-9]+)/new$', AddThemeView.as_view(), name='new'),
    url(r'^(?P<theme>[0-9]+)/edit$', EditThemeView.as_view(), name='edit'),
]
