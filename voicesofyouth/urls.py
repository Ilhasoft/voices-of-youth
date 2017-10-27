from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('voicesofyouth.api.urls')),
    url(r'^voy/admin/', include('voicesofyouth.voyadmin.urls', namespace='voy-admin')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
