from django.conf.urls import url, include
from rest_framework.authtoken import views as rest_framework_views
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from .views import ProjectsEndPoint, TagsEndPoint

router = DefaultRouter()
router.register(r'projects', ProjectsEndPoint, base_name='projects')
router.register(r'tags', TagsEndPoint, base_name='tags')

urlpatterns = [
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='Voices of Youth API')),
    url(r'', include(router.urls)),
]
