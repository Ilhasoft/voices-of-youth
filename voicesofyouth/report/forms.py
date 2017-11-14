from django import forms
from django.utils.translation import ugettext as _
from voicesofyouth.report.models import REPORT_STATUS_CHOICES
from voicesofyouth.project.models import Project
from voicesofyouth.tag.models import Tag


class MyModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name


class ReportForm(forms.Form):
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
        choices=Tag.objects.all().values_list('id', 'name'),
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

    theme = forms.CharField(
        label=_('Theme'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    mapper = forms.CharField(
        label=_('Mapper'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    location = forms.CharField(
        label=_('Location'),
        required=True,
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)


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
