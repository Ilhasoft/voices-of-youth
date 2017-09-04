from django.contrib import admin

from .models import Report, ReportLanguage, ReportTags, ReportFavoriteBy, ReportComments


class ReportAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'map_name', 'theme_name', 'location', 'sharing', 'comments', 'editable', 'enabled', 'visibled')

    def project_name(self, obj):
        return obj.project.name

    def map_name(self, obj):
        return obj.map.name

    def theme_name(self, obj):
        return obj.theme.name


class ReportLanguageAdmin(admin.ModelAdmin):
    list_display = ('theme_name', 'language', 'title', 'description')

    def theme_name(self, obj):
        return obj.report.theme.name


class ReportTagsAdmin(admin.ModelAdmin):
    list_display = ('theme_name', 'tag_name')

    def theme_name(self, obj):
        return obj.report.theme.name

    def tag_name(self, obj):
        return obj.tag.name


class ReportFavoriteByAdmin(admin.ModelAdmin):
    list_display = ('theme_name', 'user_name')

    def theme_name(self, obj):
        return obj.report.theme.name

    def user_name(self, obj):
        return obj.created_by.display_name


class ReportCommentsAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'body', 'user_name')

    def project_name(self, obj):
        return obj.project.name

    def user_name(self, obj):
        return obj.created_by.display_name


admin.site.register(Report, ReportAdmin)
admin.site.register(ReportLanguage, ReportLanguageAdmin)
admin.site.register(ReportTags, ReportTagsAdmin)
admin.site.register(ReportFavoriteBy, ReportFavoriteByAdmin)
admin.site.register(ReportComments, ReportCommentsAdmin)
