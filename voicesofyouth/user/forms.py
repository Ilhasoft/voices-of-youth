from django import forms
from django.utils.translation import ugettext as _

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme
from voicesofyouth.theme.forms import ThemesWidget
from voicesofyouth.user.models import AVATARS
from voicesofyouth.user.models import DEFAULT_AVATAR
from voicesofyouth.user.models import VoyUser
from voicesofyouth.user.models import MapperUser
from voicesofyouth.user.models import AdminUser


class MapperFilterForm(forms.Form):
    project = forms.ModelChoiceField(queryset=None,
                                     required=False,
                                     widget=forms.Select(
                                         attrs={'class': 'select_project_id'}
                                     ),
                                     empty_label=_('Select a project'))
    theme = forms.ModelChoiceField(required=False,
                                   queryset=None,
                                   widget=forms.Select(choices=[],
                                                       attrs={'class': 'select_themes_id'}
                                                       ))
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Search for mappers'),
                                                           'class': 'form-control'}),
                             required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_qs = Project.objects.filter(themes__reports__isnull=False).distinct()
        self.fields['project'].queryset = project_qs

        if 'project' in kwargs.get('initial'):
            project_id = kwargs.get('initial')['project']
            theme_qs = Theme.objects.filter(project__id=project_id).distinct()
            self.fields['theme'].queryset = theme_qs
        else:
            self.fields['theme'].queryset = Theme.objects.none()


class AdminFilterForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Search for admin users'),
                                                           'class': 'form-control'}),
                             required=False)


class VoyUserBaseForm(forms.ModelForm):
    class Meta:
        model = VoyUser
        fields = [
            'username',
            'email',
            'avatar',
            'first_name',
            'last_name',
        ]

    username = forms.CharField(max_length=32,
                               label=_('Username'),
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control required',
                                       'placeholder': _('Set the username that will use to Log in to the Voy project.'),
                                       'autocomplete': 'off'
                                   },
                               ))
    email = forms.EmailField(required=False,
                             label=_('E-mail'),
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control',
                                     'autocomplete': 'off'
                                 }
                             ))
    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control required',
                                       'id': 'password-form',
                                       'autocomplete': 'off'}))
    name = forms.CharField(max_length=255,
                           label=_('Name'),
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control required',
                                   'placeholder': _('Set the User full name'),
                                   'autocomplete': 'off'
                               },
                           ))
    first_name = forms.CharField(required=False,
                                 widget=forms.HiddenInput())
    last_name = forms.CharField(required=False,
                                widget=forms.HiddenInput())
    avatar = forms.ChoiceField(choices=AVATARS,
                               initial=DEFAULT_AVATAR,
                               widget=forms.HiddenInput())

    field_order = [
        'username',
        'email',
        'password',
        'name',
    ]

    def __init__(self, *args, instance=None, initial=None, **kwargs):
        if instance:
            if not initial:
                initial = {}
            initial.update({
                'name': instance.get_full_name(),
                'projects': instance.projects.all()
            })
        super().__init__(*args, instance=instance, initial=initial, **kwargs)
        if instance:
            self.fields.pop('password')

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        name = cleaned_data.get('name')
        try:
            first_name, last_name = name.split(maxsplit=1)
        except ValueError:
            first_name = name
            last_name = ''
        cleaned_data['first_name'] = first_name
        cleaned_data['last_name'] = last_name
        return cleaned_data

    def save(self, commit=True):
        super().save(commit=commit)
        password = self.cleaned_data.get('password')
        if password:
            self.instance.set_password(password)
            if commit:
                self.instance.save()


class MapperForm(VoyUserBaseForm):
    class Meta:
        model = MapperUser
        fields = VoyUserBaseForm.Meta.fields

    projects = forms.ModelMultipleChoiceField(queryset=Project.objects,
                                              label=_('Project'),
                                              required=False,
                                              widget=forms.SelectMultiple(
                                                  attrs={
                                                      'multiple': True,
                                                      'class': 'chosen-select form-control',
                                                      'data-placeholder': _('Select one or more projects'),
                                                  }
                                              ))
    themes = forms.ModelMultipleChoiceField(queryset=Theme.objects.none(),
                                            label=_('Themes'),
                                            required=False,
                                            widget=ThemesWidget(
                                                attrs={
                                                    'multiple': True,
                                                    'class': 'chosen-select form-control',
                                                    'data-placeholder': _('Select one or more themes'),
                                                }))

    def __init__(self, *args, instance=None, initial=None, **kwargs):
        if instance:
            if not initial:
                initial = {}
            initial.update({
                'themes': instance.themes,
            })

        super().__init__(*args, instance=instance, initial=initial, **kwargs)

        if self.data.get('themes'):
            projects = Project.objects.filter(themes__id__in=self.data.get('themes'))
        elif instance:
            projects = instance.projects
        else:
            projects = []

        self.fields['themes'].queryset = Theme.objects.filter(project__in=projects)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        themes = self.cleaned_data.get('themes')

        # Remove mapper from a group.
        for group in self.instance.groups.exclude(theme_mappers__id__in=themes):
            group.user_set.remove(self.instance)

        # Add mapper to a group
        for theme in themes:
            theme.mappers_group.user_set.add(self.instance)

        return self.instance


class AdminForm(VoyUserBaseForm):
    class Meta:
        model = AdminUser
        fields = VoyUserBaseForm.Meta.fields

    global_admin = forms.ChoiceField(choices=[('global', 'Global admin'), ('local', 'Local admin')],
                                     widget=forms.RadioSelect(
                                         attrs={
                                             'class': 'admin-profile-selector radio-inline'
                                         }
    ),
        label=_('Profile'))
    projects = forms.ModelMultipleChoiceField(queryset=Project.objects.all(),
                                              label=_('Project'),
                                              required=False,
                                              widget=forms.SelectMultiple(
                                                  attrs={
                                                      'multiple': True,
                                                      'class': 'chosen-select form-control'}))

    def __init__(self, *args, instance=None, initial=None, **kwargs):
        if instance:
            if not initial:
                initial = {}
            initial.update({
                'global_admin': 'global' if instance.is_superuser else 'local',
                'projects': instance.projects.all(),
            })
        super().__init__(*args, instance=instance, initial=initial, **kwargs)

    def save(self, *args, commit=True, **kwargs):
        super().save(*args, **kwargs)

        global_admin = self.cleaned_data.get('global_admin')
        projects = self.cleaned_data.get('projects')

        self.instance.is_superuser = global_admin == 'global'
        if commit:
            self.instance.save()

        for project in self.instance.projects.all():
            project.local_admin_group.user_set.remove(self.instance)

        if global_admin == 'local':
            for project in projects:
                project.local_admin_group.user_set.add(self.instance)

    def clean(self):
        cleaned_data = super().clean()
        global_admin = cleaned_data.get('global_admin')
        projects = cleaned_data.get('projects')

        if global_admin != 'global' and not projects:
            self.add_error('projects', _('You must inform at least one theme for local admin.'))

        return cleaned_data


class UserResetPasswordForm(forms.Form):
    reset_password = forms.CharField(widget=forms.HiddenInput(
        attrs={
            'value': 'reset_password'
        }
    ))

    password = forms.CharField(min_length=6, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ), required=True)

    confirm_password = forms.CharField(min_length=6, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ), required=True)
