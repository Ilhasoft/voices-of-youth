from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Project
from .models import ProjectTranslation


class ProjectAdmin(BaseModelAdmin):
    list_display = ('name', 'path', 'language')


class ProjectTranslationAdmin(BaseModelAdmin):
    list_display = ('project_name', 'language', 'name', 'window_title')

    def project_name(self, obj):
        return obj.settings.project.name


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTranslation, ProjectTranslationAdmin)
