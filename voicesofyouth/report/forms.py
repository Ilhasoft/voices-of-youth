from django import forms
from django.utils.translation import ugettext as _
from voicesofyouth.report.models import REPORT_STATUS_CHOICES


class MyModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name


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
