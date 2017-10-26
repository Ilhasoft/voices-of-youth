from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Theme


class ThemeAdmin(BaseModelAdmin):
    list_display = ('name', 'project_name', 'visible', 'is_active')

    def project_name(self, obj):
        return obj.project.name


admin.site.register(Theme, ThemeAdmin)
