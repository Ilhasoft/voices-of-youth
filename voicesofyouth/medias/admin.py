from django.contrib import admin

from .models import Media


class MediaAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'report_name', 'title', 'description', 'media_type', 'language', 'is_active', 'visibled')

    def project_name(self, obj):
        return obj.project.name

    def report_name(self, obj):
        return obj.report.theme.name


admin.site.register(Media, MediaAdmin)
