from django.contrib import admin

from voicesofyouth.translation.models import TranslatableModel
from voicesofyouth.translation.models import TranslatableField
from voicesofyouth.translation.models import Translation


class TranstableModelAdmin(admin.ModelAdmin):
    list_display = ('model', 'verbose_name', 'verbose_name_plural')
    readonly_fields = list_display


class TranslatableFieldAdmin(admin.ModelAdmin):
    list_display = ('model', 'field_name', 'verbose_name')
    readonly_fields = list_display


class TranslationAdmin(admin.ModelAdmin):
    list_display = ('field', 'language', 'content_object', 'translation')
    list_editable = ('language', 'translation')
    list_filter = ('language', 'field')


admin.site.register(TranslatableModel, TranstableModelAdmin)
admin.site.register(TranslatableField, TranslatableFieldAdmin)
admin.site.register(Translation, TranslationAdmin)
