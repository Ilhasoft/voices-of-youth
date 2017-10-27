from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from voicesofyouth.report.admin_filter import ThemeListFilter
from .models import Report
from .models import ReportComment
from .models import ReportFile
from .models import ReportURL


class ReportAdmin(BaseModelAdmin):
    list_display = (
        'project',
        'theme',
        'location',
        'name',
        'description',
        'can_receive_comments',
        'editable',
        'visible',
        'status',
        'tags_name',
    )
    list_filter = (
        'theme__project',
        ThemeListFilter,
        'can_receive_comments',
        'editable',
        'visible',
        'status',
        'tags'
    )

    def tags_name(self, obj):
        return list(obj.tags.names()) or ''
    tags_name.visible_name = 'tags'


class ReportCommentAdmin(BaseModelAdmin):
    list_display = ('text', 'author')
    list_filter = ('report__theme__project', ThemeListFilter)


class ReportURLAdmin(BaseModelAdmin):
    list_display = ('url', 'report')
    list_filter = ('report__theme__project', ThemeListFilter)


class ReportFileAdmin(BaseModelAdmin):
    list_display = (
        'title',
        'media_type',
        'file',
        'report',
        'description',
    )
    list_filter = ('report__theme__project', ThemeListFilter)


admin.site.register(Report, ReportAdmin)
admin.site.register(ReportComment, ReportCommentAdmin)
admin.site.register(ReportURL, ReportURLAdmin)
admin.site.register(ReportFile, ReportFileAdmin)
