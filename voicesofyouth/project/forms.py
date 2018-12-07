from django import forms
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _

from leaflet.forms.fields import PolygonField

from .models import Project

from voicesofyouth.core.tools.image import validate_file_extension
from voicesofyouth.user.models import VoyUser
from voicesofyouth.translation.forms import TranslationsField


class ProjectForm(forms.Form):
    name = forms.CharField(
        label=_('Name'),
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Add a project name'),
                'required': True,
                'class': 'form-control',
            }
        )
    )

    description = forms.CharField(
        label=_('Path'),
        required=True,
        widget=forms.Textarea(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    language = forms.ChoiceField(
        choices=django_settings.LANGUAGES,
        label=_('Language'),
        required=True,
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    path = forms.CharField(
        label=_('Path'),
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Path'),
                'required': False,
                'class': 'form-control',
            }
        )
    )

    bounds = PolygonField(
        required=True
    )

    tags = forms.CharField(
        label=_('Tags'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'class': 'form-control',
                'placeholder': _('Type and press enter to create Tags'),
            }
        )
    )

    local_admin = forms.ModelMultipleChoiceField(
        queryset=None,
        label=_('Local Admin'),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'required': False,
                'multiple': True,
                'class': 'form-control',
                'data-placeholder': _('Select one or more local admins to this project'),
            }
        )
    )

    thumbnail = forms.FileField(
        label=_('Thumbnail'),
        required=True,
        validators=[validate_file_extension],
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    enabled = forms.BooleanField(
        label=_('Enabled'),
        required=False
    )

    enabled_in_signup_form = forms.BooleanField(
        label=_('View in sign up form'),
        required=False
    )

    translations = TranslationsField(
        Project,
        label=_('Languages'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        on_edit = kwargs.get('on_edit', False)
        if 'on_edit' in kwargs:
            kwargs.pop('on_edit')

        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['local_admin'].queryset = VoyUser.objects.filter(groups__name__contains='- local admin').distinct()

        if on_edit:
            self.fields['thumbnail'].required = False

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        bounds = cleaned_data.get('bounds')

        if bounds is None:
            raise forms.ValidationError(_('Bounds is empty'))


class ProjectTranslationForm(forms.Form):
    language = forms.ChoiceField(
        choices=django_settings.LANGUAGES,
        label=_('Language'),
        required=True,
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    name = forms.CharField(
        label=_('Name'),
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )
