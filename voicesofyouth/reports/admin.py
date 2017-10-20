from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Report
from .models import ReportLanguage
from .models import ReportFavoriteBy
from .models import ReportComments
from .models import ReportMedias


class ReportAdmin(BaseModelAdmin):
    list_display = ('project_name', 'map_name', 'theme_name', 'location', 'sharing', 'comments', 'editable', 'is_active', 'visibled')

    def project_name(self, obj):
        return obj.project.name

    def map_name(self, obj):
        return obj.map.name

    def theme_name(self, obj):
        return obj.theme.name


class ReportLanguageAdmin(BaseModelAdmin):
    list_display = ('theme_name', 'language', 'title', 'description')

    def theme_name(self, obj):
        return obj.report.theme.name


class ReportFavoriteByAdmin(BaseModelAdmin):
    list_display = ('theme_name', 'user_name')

    def theme_name(self, obj):
        return obj.report.theme.name

    def user_name(self, obj):
        return obj.created_by.display_name


class ReportCommentsAdmin(BaseModelAdmin):
    list_display = ('body', 'user_name')

    def user_name(self, obj):
        return obj.created_by.display_name


class ReportMediasAdmin(BaseModelAdmin):
    list_display = ('title', 'description', 'media_type', 'language', 'is_active', 'visibled')


admin.site.register(Report, ReportAdmin)
admin.site.register(ReportLanguage, ReportLanguageAdmin)
admin.site.register(ReportFavoriteBy, ReportFavoriteByAdmin)
admin.site.register(ReportComments, ReportCommentsAdmin)
admin.site.register(ReportMedias, ReportMediasAdmin)
