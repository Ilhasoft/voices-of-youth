from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings as django_settings

from leaflet.forms.fields import PolygonField

from voicesofyouth.user.models import MapperUser

from voicesofyouth.translation.forms import TranslationsField
from .models import Theme


class MyModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name


class ThemeForm(forms.Form):
    date_format = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%m/%d/%y',
        '%d/%m/%Y'
    ]

    name = forms.CharField(
        label=_('Name'),
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Enter the theme\'s name belonging to this project.'),
                'required': True,
                'class': 'form-control',
            }
        )
    )

    description = forms.CharField(
        label=_('Search'),
        required=True,
        widget=forms.Textarea(
            attrs={
                'cols': 40,
                'rows': 5,
                'required': True,
                'class': 'form-control',
            }
        )
    )

    tags = forms.MultipleChoiceField(
        choices=[],
        label=_('Tags'),
        required=True,
        widget=forms.SelectMultiple(
            attrs={
                'required': True,
                'multiple': True,
                'class': 'chosen-select form-control',
                'data-placeholder': _('Select one or more Tags for Mappers to use.'),
            }
        )
    )

    start_at = forms.DateField(
        label=_('Start'),
        required=False,
        input_formats=date_format,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control startdatepicker',
            }
        )
    )

    end_at = forms.DateField(
        label=_('End'),
        required=False,
        input_formats=date_format,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control expiredatepicker',
            }
        )
    )

    visible = forms.BooleanField(
        label=_('Visible'),
        required=False
    )

    allow_links = forms.BooleanField(
        label=_('Allow mappers to add links to reports'),
        required=False
    )

    color = forms.CharField(
        required=True,
        widget=forms.HiddenInput()
    )

    bounds = PolygonField(
        required=False
    )

    mappers_group = forms.ModelMultipleChoiceField(
        queryset=None,
        label=_('Mappers'),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'required': True,
                'multiple': True,
                'class': 'form-control',
                'data-placeholder': _('Select one or more mappers who will create reports here.'),
            }
        )
    )

    translations = TranslationsField(
        Theme,
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
        project = kwargs.pop('project')
        super(ThemeForm, self).__init__(*args, **kwargs)
        self.fields['tags'].choices = project.all_tags.values_list('name', 'name')

        groups_ids = project.themes.values_list('mappers_group__id')
        qs = MapperUser.objects.filter(groups__id__in=groups_ids)
        self.fields['mappers_group'].queryset = qs

class ThemeTranslationForm(forms.Form):
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
