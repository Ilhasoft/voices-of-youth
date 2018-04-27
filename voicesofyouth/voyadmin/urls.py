from django.conf.urls import include
from django.conf.urls import url

from voicesofyouth.voyadmin.views import DashboardView
from voicesofyouth.voyadmin.views import LoginView
from voicesofyouth.voyadmin.views import logout

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^projects/', include('voicesofyouth.project.urls', namespace='projects')),
    url(r'^themes/', include('voicesofyouth.theme.urls', namespace='themes')),
    url(r'^reports/', include('voicesofyouth.report.urls', namespace='reports')),
    url(r'^users/', include('voicesofyouth.user.urls', namespace='users')),
    url(r'^home/', include('voicesofyouth.voyhome.urls', namespace='home')),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', logout, name='logout'),
]
