from django import forms
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone

from leaflet.forms.fields import PointField

from voicesofyouth.report.models import REPORT_STATUS_CHOICES
from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme
from voicesofyouth.tag.models import Tag


class MyModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name


class ReportForm(forms.Form):
    project = MyModelChoiceField(
        queryset=Project.objects.all(),
        label=_('Project'),
        empty_label=_('Select a project'),
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
                'placeholder': _('Define a title'),
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
                'cols': 40,
                'rows': 5,
                'required': True,
                'class': 'form-control',
                'placeholder': _('Describe your report freely'),
            }
        )
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        label=_('Tags'),
        required=True,
        widget=forms.SelectMultiple(
            attrs={
                'required': True,
                'multiple': True,
                'class': 'chosen-select form-control',
                'data-placeholder': _('Select one or more Tags to compose this report'),
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

    location = PointField(
        required=True
    )

    link = forms.CharField(
        label=_('Links from website'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Type or paste some valid url to this report'),
                'required': False,
                'class': 'form-control',
            }
        )
    )

    files = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ReportForm, self).__init__(*args, **kwargs)

        if not self.user.is_global_admin:
            self.fields['project'].queryset = self.user.projects.all()

        theme_id = self.data.get('theme', self.initial.get('project'))
        if theme_id:
            ct_theme = ContentType.objects.get_for_model(Theme)

            self.fields['tags'].queryset = Tag.objects.filter(
                taggit_taggeditem_items__content_type=ct_theme,
                taggit_taggeditem_items__object_id=theme_id).distinct()

    def clean_location(self):
        theme_id = self.cleaned_data.get('theme')
        if theme_id:
            theme = Theme.objects.get(id=theme_id)
            if not theme.bounds.contains(self.cleaned_data['location']):
                msg = _(f'You cannot create a report outside the theme bounds.')
                raise forms.ValidationError(msg)

        return self.cleaned_data['location']

    def clean_theme(self):
        theme_id = self.cleaned_data.get('theme')
        theme = Theme.objects.get(id=theme_id)
        if theme.start_at and theme.end_at:
            if theme.start_at > timezone.localdate() or theme.end_at < timezone.localdate():
                msg = _(f'You cannot create a report out of the theme period.')
                raise forms.ValidationError(msg)
        return theme_id


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
                'placeholder': _('Project name'),
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


class ReportPendingFilterForm(forms.Form):
    project = MyModelChoiceField(queryset=None,
                                 required=False,
                                 empty_label='Project',
                                 widget=forms.Select(attrs={'class': 'form-control m-b'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ReportPendingFilterForm, self).__init__(*args, **kwargs)

        if self.user.is_global_admin:
            self.fields['project'].queryset = Project.objects.all()
        else:
            self.fields['project'].queryset = self.user.projects.all()
