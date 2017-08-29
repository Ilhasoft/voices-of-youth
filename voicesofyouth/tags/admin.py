from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'name', 'system_tag', 'urgency_score')

    def country_name(self, obj):
        return obj.country.name


admin.site.register(Tag, TagAdmin)
