from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ('modified_by', 'created_by')

    def save_model(self, request, obj, form, change):
        '''
        This method ensures the fields modified_by and created_by are filled correctly.
        '''
        if hasattr(obj, 'modified_by_id'):
            obj.modified_by_id = request.user.id

        if not change and hasattr(obj, 'created_by_id'):
            obj.created_by_id = request.user.id
        super().save_model(request, obj, form, change)
