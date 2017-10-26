from django.contrib import admin

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Report
from .models import ReportComment
from .models import ReportMedia


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


class ReportCommentAdmin(BaseModelAdmin):
    list_display = ('text', 'user_name')

    def user_name(self, obj):
        return obj.created_by.display_name


class ReportMediaAdmin(BaseModelAdmin):
    list_display = ('title', 'description', 'media_type', 'is_active', 'visible')


admin.site.register(Report, ReportAdmin)
admin.site.register(ReportComment, ReportCommentAdmin)
admin.site.register(ReportMedia, ReportMediaAdmin)
