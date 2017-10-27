from django.contrib import admin

from voicesofyouth.theme.models import Theme


class ThemeListFilter(admin.SimpleListFilter):
    title = 'Theme'
    parameter_name = 'theme'

    def lookups(self, request, model_admin):
        filter_params = {}
        if 'report__theme__project__id__exact' in request.GET.keys():
            filter_params['project__id'] = request.GET.get('report__theme__project__id__exact')
        if 'theme__project__id__exact' in request.GET.keys():
            filter_params['project__id'] = request.GET.get('theme__project__id__exact')
        return Theme.objects.filter(**filter_params).order_by('name').distinct().values_list('id', 'name')

    def queryset(self, request, queryset):
        if 'theme__project__id__exact' in request.GET.keys() and self.value():
            return queryset.filter(theme__id=self.value())
        elif self.value():
            return queryset.filter(report__theme__id=self.value())
        return queryset
