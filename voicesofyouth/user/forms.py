from django import forms
from django.utils.translation import ugettext as _

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import AVATARS


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


class AdminFilterForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Search for admin users'),
                                                           'class': 'form-control'}),
                             required=False)


class VoyUserBaseForm(forms.Form):
    username = forms.CharField(max_length=32,
                               label=_('Username'),
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control'
                                   },
                               ))
    name = forms.CharField(max_length=255,
                           label=_('Name'),
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control'
                               },
                           ))
    email = forms.EmailField(required=False,
                             label=_('E-mail'),
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
    avatars = forms.ChoiceField(choices=AVATARS,
                                widget=forms.HiddenInput())

    def save(self, user):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            name = cleaned_data.get('name')
            email = cleaned_data.get('email')
            username = cleaned_data.get('username')
            themes = cleaned_data.get('themes')

            # set name
            if len(name.split()) > 1:
                user.first_name, user.last_name = name.split(maxsplit=1)
            else:
                user.first_name = name

            user.email = email
            user.username = username
            user.save()
            return True
        else:
            return False


class MapperForm(VoyUserBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.all()
        self.fields['themes'].queryset = Theme.objects.all()

    def save(self, mapper):
        if super().save(mapper):
            # set mappers group
            # Admin user remove mapper from a group.
            for group in user.groups.exclude(theme_mappers__id__in=themes):
                group.user_set.remove(user)
            # Admin user add mapper to a group
            for theme in Theme.objects.filter(id__in=themes):
                theme.mappers_group.user_set.add(user)

            return True
        else:
            return False


class AdminForm(forms.Form):
    username = forms.CharField(max_length=32,
                           label=_('Username'),
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control'
                               },
                           ))
    name = forms.CharField(max_length=255,
                           label=_('Name'),
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control'
                               },
                           ))
    email = forms.EmailField(required=False,
                             label=_('E-mail'),
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
    avatars = forms.ChoiceField(choices=AVATARS,
                                widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.all()
        self.fields['themes'].queryset = Theme.objects.all()

    def save(self, admin):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            name = cleaned_data.get('name')
            email = cleaned_data.get('email')
            username = cleaned_data.get('username')
            themes = cleaned_data.get('themes')

            # set name
            if len(name.split()) > 1:
                admin.first_name, admin.last_name = name.split(maxsplit=1)
            else:
                admin.first_name = name

            admin.email = email
            admin.username = username
            admin.save()

            # set mappers group
            # Admin user remove mapper from a group.
            for group in admin.groups.exclude(theme_mappers__id__in=themes):
                group.user_set.remove(admin)
            # Admin user add mapper to a group
            for theme in Theme.objects.filter(id__in=themes):
                theme.mappers_group.user_set.add(admin)

            return True
        else:
            return False

