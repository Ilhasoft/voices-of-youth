from django.contrib import admin

from .models import Theme, ThemeLanguage, ThemeTags, ThemeFavoriteBy


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


class ThemeTagsAdmin(admin.ModelAdmin):
    list_display = ('theme_name', 'tag_name')

    def theme_name(self, obj):
        return obj.theme.name

    def tag_name(self, obj):
        return obj.tag.name


class ThemeFavoriteByAdmin(admin.ModelAdmin):
    list_display = ('theme_name', 'user_name')

    def theme_name(self, obj):
        return obj.theme.name

    def user_name(self, obj):
        return obj.created_by.display_name


admin.site.register(Theme, ThemeAdmin)
admin.site.register(ThemeLanguage, ThemeLanguageAdmin)
admin.site.register(ThemeTags, ThemeTagsAdmin)
admin.site.register(ThemeFavoriteBy, ThemeFavoriteByAdmin)
