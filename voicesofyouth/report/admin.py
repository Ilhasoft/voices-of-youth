from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Report
from .models import ReportLanguage
from .models import ReportComments
from .models import ReportMedias


class ReportAdmin(BaseModelAdmin):
    list_display = (
        'project',
        'theme',
        'location',
        'name',
        'description',
        'comments',
        'editable',
        'visible',
        'status',
        'tags_name',
    )

    def tags_name(self, obj):
        return list(obj.tags.names()) or ''
    tags_name.visible_name = 'tags'


class ReportLanguageAdmin(BaseModelAdmin):
    list_display = ('theme_name', 'language', 'title', 'description')

    def theme_name(self, obj):
        return obj.report.theme.name


class ReportCommentsAdmin(BaseModelAdmin):
    list_display = ('body', 'user_name')

    def user_name(self, obj):
        return obj.created_by.display_name


class ReportMediasAdmin(BaseModelAdmin):
    list_display = ('title', 'description', 'media_type', 'language', 'is_active', 'visibled')


admin.site.register(Report, ReportAdmin)
admin.site.register(ReportLanguage, ReportLanguageAdmin)
admin.site.register(ReportComments, ReportCommentsAdmin)
admin.site.register(ReportMedias, ReportMediasAdmin)
