from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme


class ProjectListFilter(admin.SimpleListFilter):
    title = 'Project'
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        return Project.objects.all().order_by('name').distinct().values_list('id', 'name')

    def queryset(self, request, queryset):
        project_id = int(request.GET.get('project', 0))
        theme_id = int(request.GET.get('theme', 0))
        filter_by_project = {}
        filter_by_theme = {}
        try:
            project = Project.objects.get(id=project_id)
            theme = Theme.objects.get(id=theme_id)
            project_ct = ContentType.objects.get_for_model(project)
            theme_ct = ContentType.objects.get_for_model(theme)
            filter_by_project = {'content_type': project_ct, 'object_id': project_id}
            filter_by_theme = {'content_type': theme_ct, 'object_id': theme_id}
        except Project.DoesNotExist:
            pass
        return queryset.filter(Q(**filter_by_project) | Q(**filter_by_theme))


class ThemeListFilter(admin.SimpleListFilter):
    title = 'Theme'
    parameter_name = 'theme'

    def lookups(self, request, model_admin):
        filter_params = {}
        if 'project' in request.GET.keys():
            filter_params['project__id'] = int(request.GET.get('project'))
        return Theme.objects.filter(**filter_params).order_by('name').distinct().values_list('id', 'name')

    def queryset(self, request, queryset):
        theme_id = int(request.GET.get('theme', 0))
        filter_clause = {}
        try:
            theme = Theme.objects.get(id=theme_id)
            ct = ContentType.objects.get_for_model(theme)
            filter_clause = {'content_type': ct, 'object_id': theme_id}
        except Theme.DoesNotExist:
            pass
        return queryset.filter(**filter_clause)
