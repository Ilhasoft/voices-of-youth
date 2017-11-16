from django import forms
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _


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
        max_length=255,
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

    window_title = forms.CharField(
        label=_('Window Title'),
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Window Title'),
                'required': True,
                'class': 'form-control',
            }
        )
    )

    boundary = forms.HiddenInput()

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

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # self.fields['project'].queryset = Project.objects.all()
        # self.fields['tags'].choices = Tag.objects.all().values_list('name', 'name')
