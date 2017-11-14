from django.conf.urls import include
from django.conf.urls import url
from rest_framework.authtoken import views as rest_framework_views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from voicesofyouth.api.v1.mapper.views import MappersEndPoint
from voicesofyouth.api.v1.report.views import ReportCommentsViewSet, ReportURLsViewSet, ReportMediasViewSet
from voicesofyouth.api.v1.report.views import ReportFilesViewSet
from voicesofyouth.api.v1.report.views import ReportsViewSet
from voicesofyouth.api.v1.tag.views import TagsViewSet
from voicesofyouth.api.v1.user.views import UsersEndPoint
from .project.views import ProjectsViewSet
from .theme.views import ThemesViewSet

router = DefaultRouter()
router.register(r'projects', ProjectsViewSet, base_name='projects')
router.register(r'themes', ThemesViewSet, base_name='themes')
router.register(r'tags', TagsViewSet, base_name='tags')
router.register(r'users', UsersEndPoint, base_name='users')
router.register(r'mappers', MappersEndPoint, base_name='mappers')
router.register(r'reports', ReportsViewSet, base_name='reports')
router.register(r'report-comments', ReportCommentsViewSet, base_name='report-comments')
router.register(r'report-medias', ReportMediasViewSet, base_name='report-medias')
router.register(r'report-files', ReportFilesViewSet, base_name='report-files')
router.register(r'report-urls', ReportURLsViewSet, base_name='report-urls')

urlpatterns = [
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='Voices of Youth API')),
    url(r'', include(router.urls, namespace='voy-api')),
    # url(r'^comments/$', CommentsEndPoint.as_view()),
]
