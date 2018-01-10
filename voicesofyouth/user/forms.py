from django import forms
from django.utils.translation import ugettext as _

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import AVATARS
from voicesofyouth.user.models import DEFAULT_AVATAR


class MapperFilterForm(forms.Form):
    project = forms.ModelChoiceField(queryset=None,
                                     required=False,
                                     widget=forms.Select())
    theme = forms.ModelChoiceField(queryset=None,
                                   required=False,
                                   widget=forms.Select())
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
    avatars = forms.ChoiceField(choices=AVATARS,
                                initial=DEFAULT_AVATAR,
                                widget=forms.HiddenInput())

    def save(self, user):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            name = cleaned_data.get('name')
            email = cleaned_data.get('email')
            username = cleaned_data.get('username')
            avatar = cleaned_data.get('avatars')

            if len(name.split()) > 1:
                user.first_name, user.last_name = name.split(maxsplit=1)
            else:
                user.first_name = name

            user.email = email
            user.username = username
            user.avatar = avatar
            user.save()
            return True
        else:
            return False


class MapperForm(VoyUserBaseForm):
    project = forms.ModelChoiceField(queryset=None,
                                     label=_('Project'),
                                     required=False,
                                     widget=forms.Select(
                                         attrs={
                                             'class': 'form-control',
                                         }
                                     ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.all()

    def save(self, mapper, themes):
        if super().save(mapper):
            # Remove mapper from a group.
            for group in mapper.groups.exclude(theme_mappers__id__in=themes):
                group.user_set.remove(mapper)

            # Add mapper to a group
            for theme in Theme.objects.filter(id__in=themes):
                theme.mappers_group.user_set.add(mapper)

            return True
        else:
            return False


class AdminForm(VoyUserBaseForm):
    global_admin = forms.ChoiceField(choices=(('global', 'Global admin'), ('local', 'Local admin')),
                                     widget=forms.RadioSelect(
                                         attrs={
                                             'class': 'admin-profile-selector radio-inline'
                                         }
    ),
        label=_('Profile'))
    projects = forms.ModelMultipleChoiceField(queryset=None,
                                              label=_('Project'),
                                              required=False,
                                              widget=forms.SelectMultiple(
                                                  attrs={
                                                      'multiple': True,
                                                      'class': 'chosen-select form-control',
                                                  }
                                              ))
    field_order = ('username', 'name', 'email', 'global_admin', 'projects')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['projects'].queryset = Project.objects.all()

    def save(self, admin):
        if super().save(admin):
            global_admin = self.cleaned_data.pop('global_admin')
            projects = self.cleaned_data.pop('projects')
            for field, value in self.cleaned_data.items():
                setattr(admin, field, value)
            admin.is_superuser = global_admin == 'global'
            admin.save()
            for project in projects:
                project.local_admin_group.user_set.add(admin)
            return True
        else:
            return False

    def clean(self):
        global_admin = self.cleaned_data['global_admin']
        projects = self.cleaned_data.get('projects')

        if global_admin != 'global' and not projects:
            self.add_error('projects', _('You must inform at least one theme for local admin.'))

        return self.cleaned_data
