from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Map


class MapAdmin(BaseModelAdmin):
    list_display = ('name', 'project_name', 'is_active', 'bounds')

    def project_name(self, obj):
        return obj.project.name


admin.site.register(Map, MapAdmin)
