from django import forms
from django.utils.translation import ugettext as _


class SlideForm(forms.Form):
    image = forms.FileField(
        label=_('Image'),
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(SlideForm, self).__init__(*args, **kwargs)


class AboutForm(forms.Form):
    image = forms.FileField(
        label=_('Image'),
        required=True,
        widget=forms.FileInput(
            attrs={
                'required': False,
                'class': 'form-control',
            }
        )
    )

    about_project = forms.CharField(
        label=_('About The Project'),
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

    about_voy = forms.CharField(
        label=_('About Voices of Youth'),
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

    def __init__(self, *args, **kwargs):
        super(AboutForm, self).__init__(*args, **kwargs)
