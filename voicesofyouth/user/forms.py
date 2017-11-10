from django import forms

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme


class MapperFilterForm(forms.Form):
    project = forms.ModelChoiceField(queryset=None,
                                     required=False,
                                     empty_label='Project',
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    theme = forms.ModelChoiceField(queryset=None,
                                   required=False,
                                   empty_label='Theme',
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search for mappers',
                                                           'class': 'form-control'}),
                             required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_qs = Project.objects.filter(themes__reports__isnull=False).distinct()
        theme_qs = Theme.objects.filter(project__in=project_qs).distinct()
        self.fields['project'].queryset = project_qs
        self.fields['theme'].queryset = theme_qs
