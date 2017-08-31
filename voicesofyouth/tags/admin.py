from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'name', 'system_tag', 'urgency_score')

    def project_name(self, obj):
        return obj.project.name


admin.site.register(Tag, TagAdmin)
