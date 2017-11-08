from django.conf.urls import include
from django.conf.urls import url

from voicesofyouth.voyadmin.views import DashboardView

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dasboard'),
    url(r'^projects/', include('voicesofyouth.project.urls', namespace='projects')),
    url(r'^reports/', include('voicesofyouth.report.urls', namespace='reports')),
]
