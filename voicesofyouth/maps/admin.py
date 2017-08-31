from django.contrib import admin

from .models import Map


class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_name', 'enabled', 'bounds')

    def project_name(self, obj):
        return obj.project.name


admin.site.register(Map, MapAdmin)
