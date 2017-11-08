from django.conf.urls import url

from voicesofyouth.user.view import AdminView, MapperView

urlpatterns = [
    url(r'^admins/', AdminView.as_view(), name='admin'),
    url(r'^mappers/', MapperView.as_view(), name='mapper'),
]
