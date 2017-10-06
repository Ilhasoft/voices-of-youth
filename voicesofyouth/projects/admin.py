from django.contrib import admin

from .models import Project, ProjectSetting, ProjectSettingLanguage, ProjectUsers


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'language')


class ProjectSettingAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'location')

    def project_name(self, obj):
        return obj.project.name


class ProjectSettingLanguageAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'language', 'name', 'description', 'window_title')

    def project_name(self, obj):
        return obj.settings.project.name


class UsersAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'user_name')

    def project_name(self, obj):
        return obj.project.name

    def user_name(self, obj):
        return obj.user.display_name


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectSetting, ProjectSettingAdmin)
admin.site.register(ProjectSettingLanguage, ProjectSettingLanguageAdmin)
admin.site.register(ProjectUsers, UsersAdmin)
