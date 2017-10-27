from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
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

    def tags_name(self, obj):
        return list(obj.tags.names()) or ''
    tags_name.visible_name = 'tags'


class ReportCommentAdmin(BaseModelAdmin):
    list_display = ('text', 'user_name')

    def user_name(self, obj):
        return obj.created_by.display_name


class ReportURLAdmin(BaseModelAdmin):
    list_display = ('url', 'report')


class ReportFileAdmin(BaseModelAdmin):
    list_display = (
        'title',
        'media_type',
        'file',
        'report',
        'description',
    )


admin.site.register(Report, ReportAdmin)
admin.site.register(ReportComment, ReportCommentAdmin)
admin.site.register(ReportURL, ReportURLAdmin)
admin.site.register(ReportFile, ReportFileAdmin)
