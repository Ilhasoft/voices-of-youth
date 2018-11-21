from django_filters import rest_framework as filters

from voicesofyouth.project.models import Project


class ProjectFilter(filters.FilterSet):
    enabled_in_signup_form = filters.BooleanFilter(help_text='Filter enabled in form signup')

    class Meta:
        model = Project
        fields = ('enabled_in_signup_form', )
