from django import forms
from django.utils.translation import ugettext as _
from voicesofyouth.voyhome.models import About
from voicesofyouth.core.tools.image import validate_file_extension


class SlideForm(forms.Form):
    image = forms.FileField(
        label=_('Image'),
        required=True,
        validators=[validate_file_extension],
        widget=forms.ClearableFileInput(
            attrs={
                'required': True,
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(SlideForm, self).__init__(*args, **kwargs)


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = [
            'image',
            'about_project',
            'about_voy',
        ]

    image = forms.ImageField(
        label=_('Image'),
        required=True,
        widget=forms.ClearableFileInput(
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
