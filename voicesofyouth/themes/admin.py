from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Theme
from .models import ThemeLanguage
from .models import ThemeTags
from .models import ThemeFavoriteBy


class ThemeAdmin(BaseModelAdmin):
    list_display = ('project_name', 'map_name', 'name', 'visibled', 'is_active', 'cover')

    def project_name(self, obj):
        return obj.project.name

    def map_name(self, obj):
        return obj.map.name


class ThemeLanguageAdmin(BaseModelAdmin):
    list_display = ('project_name', 'theme_name', 'language', 'title', 'description')

    def project_name(self, obj):
        return obj.theme.project.name

    def theme_name(self, obj):
        return obj.theme.name


class ThemeTagsAdmin(BaseModelAdmin):
    list_display = ('theme_name', 'tag_name')

    def theme_name(self, obj):
        return obj.theme.name

    def tag_name(self, obj):
        return obj.tag.name


class ThemeFavoriteByAdmin(BaseModelAdmin):
    list_display = ('theme_name', 'user_name')

    def theme_name(self, obj):
        return obj.theme.name

    def user_name(self, obj):
        return obj.created_by.display_name


admin.site.register(Theme, ThemeAdmin)
admin.site.register(ThemeLanguage, ThemeLanguageAdmin)
admin.site.register(ThemeTags, ThemeTagsAdmin)
admin.site.register(ThemeFavoriteBy, ThemeFavoriteByAdmin)
