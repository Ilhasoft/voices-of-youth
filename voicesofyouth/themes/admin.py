from django.contrib import admin

from .models import Theme, ThemeLanguage


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'map_name', 'name', 'visibled', 'enabled', 'cover')

    def project_name(self, obj):
        return obj.project.name

    def map_name(self, obj):
        return obj.map.name


class ThemeLanguageAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'theme_name', 'language', 'title', 'description')

    def project_name(self, obj):
        return obj.theme.project.name

    def theme_name(self, obj):
        return obj.theme.name


admin.site.register(Theme, ThemeAdmin)
admin.site.register(ThemeLanguage, ThemeLanguageAdmin)
