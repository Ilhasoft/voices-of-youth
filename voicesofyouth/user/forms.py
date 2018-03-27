from django import forms
from django.utils.translation import ugettext as _

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import AVATARS
from voicesofyouth.user.models import DEFAULT_AVATAR
from voicesofyouth.user.models import VoyUser


class MapperFilterForm(forms.Form):
    project = forms.ModelChoiceField(queryset=None,
                                     required=False,
                                     widget=forms.Select(),
                                     empty_label=_('Select a project'))
    theme = forms.ModelChoiceField(queryset=None,
                                   required=False,
                                   widget=forms.Select(),
                                   empty_label=_('Select a theme'))
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
                                       'class': 'form-control',
                                       'placeholder': _('Set the username that will use to Log in to the Voy project.'),
                                       'autocomplete': 'off'
                                   },
                               ))
    name = forms.CharField(max_length=255,
                           label=_('Name'),
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'placeholder': _('Set the User full name'),
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
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'password-form',
            'autocomplete': 'off'
        }
    ), required=False)
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
            password = cleaned_data.get('password')

            if len(name.split()) > 1:
                user.first_name, user.last_name = name.split(maxsplit=1)
            else:
                user.first_name = name

            user.email = email
            user.username = username
            user.avatar = avatar
            if password is not None and password is not '':
                user.set_password(password)
            user.save()
            return True
        else:
            return False

    # TODO: Username validation
    # def clean_username(self):
    #     try:
    #         user = VoyUser.objects.get(username=self.cleaned_data['username'])
    #         if user is not None:
    #             msg = _(f'Username already exists')
    #             raise forms.ValidationError(msg)
    #     except VoyUser.DoesNotExist:
    #         pass

    #     return self.cleaned_data['username']


class MapperForm(VoyUserBaseForm):
    projects = forms.ModelMultipleChoiceField(queryset=None,
                                              label=_('Project'),
                                              required=False,
                                              widget=forms.SelectMultiple(
                                                  attrs={
                                                      'multiple': True,
                                                      'class': 'chosen-select form-control',
                                                      'data-placeholder': _('Select one or more projects'),
                                                  }
                                              ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['projects'].queryset = Project.objects.all()

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
            password = self.cleaned_data.pop('password')

            for field, value in self.cleaned_data.items():
                setattr(admin, field, value)
            admin.is_superuser = global_admin == 'global'

            if password is not None and password is not '':
                admin.set_password(password)

            admin.save()

            project_model = Project.objects.all()
            for project in project_model:
                project.local_admin_group.user_set.remove(admin)

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
