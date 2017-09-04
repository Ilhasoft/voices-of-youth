from django.contrib import admin

from .models import Project, Setting, SettingLanguage, Admin


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'language')


class SettingAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'location')

    def project_name(self, obj):
        return obj.project.name


class SettingLanguageAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'language', 'title', 'description', 'window_title')

    def project_name(self, obj):
        return obj.settings.project.name


class AdminsAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'user_name')

    def project_name(self, obj):
        return obj.project.name

    def user_name(self, obj):
        return obj.admin.display_name


admin.site.register(Project, ProjectAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(SettingLanguage, SettingLanguageAdmin)
admin.site.register(Admin, AdminsAdmin)
