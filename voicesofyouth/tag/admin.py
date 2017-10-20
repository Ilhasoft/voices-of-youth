from django.contrib import admin
from taggit.models import Tag as Taggit

from voicesofyouth.core.admin import BaseModelAdmin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'urgency_score')


admin.site.unregister(Taggit)
admin.site.register(Tag, TagAdmin)
