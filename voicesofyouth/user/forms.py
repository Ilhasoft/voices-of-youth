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
    themes = forms.ModelMultipleChoiceField(queryset=None,
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
        self.fields['themes'].queryset = Theme.objects.all()

    def save(self, mapper):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            name = cleaned_data.get('name')
            email = cleaned_data.get('email')
            themes = cleaned_data.get('themes')

            # set name
            if len(name.split()) > 1:
                mapper.first_name, mapper.last_name = name.split(maxsplit=1)
            else:
                mapper.first_name = name

            # set email
            mapper.email = email

            # set mappers group
            # Admin user remove mapper from a group.
            for group in mapper.groups.exclude(theme_mappers__id__in=themes):
                group.user_set.remove(mapper)
            # Admin user add mapper to a group
            for theme in Theme.objects.filter(id__in=themes):
                theme.mappers_group.user_set.add(mapper)

            mapper.save()
            return True
        else:
            return False

