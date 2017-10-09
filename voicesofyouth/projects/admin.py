from django.contrib import admin

from .models import Project
from .models import ProjectRegion
from .models import ProjectLanguage
from .models import ProjectUsers


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'language')


class ProjectRegionAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'region')

    def project_name(self, obj):
        return obj.project.name


class ProjectLanguageAdmin(admin.ModelAdmin):
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
admin.site.register(ProjectRegion, ProjectRegionAdmin)
admin.site.register(ProjectLanguage, ProjectLanguageAdmin)
admin.site.register(ProjectUsers, UsersAdmin)
