from django.conf.urls import url

from voicesofyouth.voyadmin.views import CoreView

urlpatterns = [
    url(r'^$', CoreView.as_view()),
]
