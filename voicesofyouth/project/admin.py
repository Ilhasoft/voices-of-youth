from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Project
from .models import ProjectRegion
from .models import ProjectTranslation


class ProjectAdmin(BaseModelAdmin):
    list_display = ('name', 'path', 'language')


class ProjectRegionAdmin(BaseModelAdmin):
    list_display = ('project_name', 'region')

    def project_name(self, obj):
        return obj.project.name


class ProjectTranslationAdmin(BaseModelAdmin):
    list_display = ('project_name', 'language', 'name', 'window_title')

    def project_name(self, obj):
        return obj.settings.project.name


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectRegion, ProjectRegionAdmin)
admin.site.register(ProjectTranslation, ProjectTranslationAdmin)
