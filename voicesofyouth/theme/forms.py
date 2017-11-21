from django import forms
from django.utils.translation import ugettext as _

from voicesofyouth.user.models import VoyUser


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
                'placeholder': _('Name'),
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
        required=True
    )

    color = forms.CharField(
        label=_('Color'),
        required=True,
        max_length=7,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control demo-colorpicker colorpicker-element',
            }
        )
    )

    boundary = forms.CharField(
        required=True,
        widget=forms.HiddenInput()
    )

    mappers_group = forms.ModelMultipleChoiceField(
        queryset=None,
        label=_('Mappers'),
        required=True,
        widget=forms.SelectMultiple(
            attrs={
                'required': True,
                'multiple': True,
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project')

        super(ThemeForm, self).__init__(*args, **kwargs)
        self.fields['tags'].choices = project.all_tags.values_list('name', 'name')
        self.fields['mappers_group'].queryset = VoyUser.objects.all()
