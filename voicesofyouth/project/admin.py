from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Project


class ProjectAdmin(BaseModelAdmin):
    list_display = ('name', 'path', 'language')


admin.site.register(Project, ProjectAdmin)
