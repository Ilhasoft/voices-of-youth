from django.contrib import admin

from .models import Boundary


class BoundaryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'title', 'bounds', 'enabled')

    def country_name(self, obj):
        return obj.country.name


admin.site.register(Boundary, BoundaryAdmin)
