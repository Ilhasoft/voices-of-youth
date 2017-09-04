from django.contrib import admin

from .models import Map, MapAdmin as MapAdminModel


class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_name', 'enabled', 'bounds')

    def project_name(self, obj):
        return obj.project.name


class MapAdminsAdmin(admin.ModelAdmin):
    list_display = ('map_name', 'user_name')

    def map_name(self, obj):
        return obj.map.name

    def user_name(self, obj):
        return obj.admin.display_name


admin.site.register(Map, MapAdmin)
admin.site.register(MapAdminModel, MapAdminsAdmin)
