from django.conf.urls import url, include
from rest_framework.authtoken import views as rest_framework_views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from .project.views import ProjectsRegionViewSet
from .project.views import ProjectsViewSet
from .views import CommentsEndPoint
from .views import MapsEndPoint, ThemesEndPoint
from .views import ReportsEndPoint
from .views import TagsEndPoint
from .views import UsersEndPoint

router = DefaultRouter()
router.register(r'projects', ProjectsViewSet, base_name='projects')
router.register(r'projects-region', ProjectsRegionViewSet, base_name='project-regions')
router.register(r'maps', MapsEndPoint, base_name='maps')
router.register(r'themes', ThemesEndPoint, base_name='themes')
router.register(r'tags', TagsEndPoint, base_name='tags')
router.register(r'users', UsersEndPoint, base_name='users')
router.register(r'reports', ReportsEndPoint, base_name='reports')
router.register(r'comments', CommentsEndPoint, base_name='comments')

urlpatterns = [
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='Voices of Youth API')),
    url(r'', include(router.urls)),
    # url(r'^comments/$', CommentsEndPoint.as_view()),
]
