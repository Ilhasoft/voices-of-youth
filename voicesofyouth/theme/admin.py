from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Theme
from .models import ThemeTranslation


class ThemeAdmin(BaseModelAdmin):
    list_display = ('project_name', 'name', 'visible', 'is_active')

    def project_name(self, obj):
        return obj.project.name


class ThemeTranslationAdmin(BaseModelAdmin):
    list_display = ('project_name', 'theme_name', 'language', 'name', 'description')

    def project_name(self, obj):
        return obj.theme.project.name

    def theme_name(self, obj):
        return obj.theme.name


admin.site.register(Theme, ThemeAdmin)
admin.site.register(ThemeTranslation, ThemeTranslationAdmin)
