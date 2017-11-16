from django import forms
from django.utils.translation import ugettext as _

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme


class MapperFilterForm(forms.Form):
    project = forms.ModelChoiceField(queryset=None,
                                     required=False,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    theme = forms.ModelChoiceField(queryset=None,
                                   required=False,
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Search for mappers'),
                                                           'class': 'form-control'}),
                             required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_qs = Project.objects.filter(themes__reports__isnull=False).distinct()
        theme_qs = Theme.objects.filter(project__in=project_qs).distinct()
        self.fields['project'].queryset = project_qs
        self.fields['theme'].queryset = theme_qs


class MapperForm(forms.Form):
    name = forms.CharField(max_length=255,
                           label=_('Name'),
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control'
                               },
                           ))
    email = forms.EmailField(required=False,
                             label=_('e-mail'),
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control'
                                 }
                             ))
    project = forms.ModelChoiceField(queryset=None,
                                     label=_('Project'),
                                     required=False,
                                     widget=forms.Select(
                                         attrs={
                                             'class': 'form-control',
                                         }
                                     ))
    themes = forms.MultipleChoiceField(choices=[],
                                       label=_('Themes'),
                                       widget=forms.SelectMultiple(
                                           attrs={
                                               'required': True,
                                               'multiple': True,
                                               'class': 'chosen-select form-control',
                                           }
                                       ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.all()
        self.fields['themes'].choices = Theme.objects.values_list('id', 'name')
