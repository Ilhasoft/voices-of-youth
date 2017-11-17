from django.conf.urls import url

from voicesofyouth.theme.view import ThemeView

urlpatterns = [
    url(r'^(?P<project>[0-9]+)/$', ThemeView.as_view(), name='index'),
]
