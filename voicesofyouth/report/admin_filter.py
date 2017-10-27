from django.contrib import admin

from voicesofyouth.theme.models import Theme


class ThemeListFilter(admin.SimpleListFilter):
    title = 'Theme'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'theme'

    def lookups(self, request, model_admin):
        print(model_admin.get_queryset(request))
        filter_params = {}
        if 'report__theme__project__id__exact' in request.GET.keys():
            filter_params['project__id'] = request.GET.get('report__theme__project__id__exact')
        return Theme.objects.filter(**filter_params).order_by('name').distinct().values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(report__theme__id=self.value())
        return queryset
