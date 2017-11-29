from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^djangoadmin/', admin.site.urls),
    url(r'^api/', include('voicesofyouth.api.urls')),
    url(r'^admin/', include('voicesofyouth.voyadmin.urls', namespace='voy-admin')),
    url(r'^docs/', include('docs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
