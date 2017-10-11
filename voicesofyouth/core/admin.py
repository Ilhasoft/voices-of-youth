from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ('modified_by', 'created_by')

    def save_model(self, request, obj, form, change):
        '''
        This method ensures the fields modified_by and created_by are filled correctly.
        '''
        if hasattr(obj, 'modified_by'):
            obj.modified_by = request.user

        if not change and hasattr(obj, 'created_by'):
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
