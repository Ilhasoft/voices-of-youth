from django import forms
from django.utils.translation import ugettext as _
from voicesofyouth.report.models import REPORT_STATUS_CHOICES
from voicesofyouth.project.models import Project


class MyModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name


class ReportFrom(forms.Form):
    project = MyModelChoiceField(
        queryset=Project.objects.all(),
        label=_('Project'),
        required=True,
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    title = forms.CharField(
        label=_('Title'),
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Title'),
                'required': True,
                'class': 'form-control',
            }
        )
    )

    description = forms.CharField(
        label=_('Search'),
        required=False,
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
        label=_('Tags'),
        required=True,
        widget=forms.Select(
            attrs={
                'required': True,
                'multiple': True,
                'class': 'chosen-select form-control',
            }
        )
    )

    theme = forms.ChoiceField(
        label=_('Theme'),
        required=True,
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    mapper = forms.ChoiceField(
        label=_('Mapper'),
        required=True,
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )


class ReportFilterForm(forms.Form):
    theme = MyModelChoiceField(queryset=None,
                               required=False,
                               empty_label='Theme',
                               widget=forms.Select(attrs={'class': 'form-control m-b'}))

    tag = MyModelChoiceField(queryset=None,
                             required=False,
                             empty_label='Tag',
                             widget=forms.Select(attrs={'class': 'form-control m-b'}))

    status = forms.ChoiceField(choices=(('', _('Status')),) + REPORT_STATUS_CHOICES,
                               required=False,
                               widget=forms.Select(attrs={'class': 'form-control m-b'}))

    search = forms.CharField(
        label=_('Search'),
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Search for report'),
                'required': False,
                'class': 'form-control ',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        theme = kwargs.pop('theme')
        super(ReportFilterForm, self).__init__(*args, **kwargs)

        self.fields['theme'].queryset = theme.project.themes.all()
        self.fields['tag'].queryset = theme.all_tags
