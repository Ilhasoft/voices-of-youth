from django.contrib import admin

from .models import Country, Setting, SettingLanguage


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'language')


class SettingAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'location')

    def country_name(self, obj):
        return obj.country.name


class SettingLanguageAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'language', 'project_title', 'project_description', 'window_title')

    def country_name(self, obj):
        return obj.settings.country.name


admin.site.register(Country, CountryAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(SettingLanguage, SettingLanguageAdmin)
