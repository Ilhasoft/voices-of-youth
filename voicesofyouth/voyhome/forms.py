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
