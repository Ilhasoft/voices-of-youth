from django import forms

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme


class MapperFilterForm(forms.Form):
    project = forms.ModelChoiceField(queryset=None, required=False)
    theme = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_qs = Project.objects.filter(themes__reports__isnull=False).distinct()
        theme_qs = Theme.objects.filter(project__in=project_qs).distinct()
        self.fields['project'].queryset = project_qs
        self.fields['theme'].queryset = theme_qs
