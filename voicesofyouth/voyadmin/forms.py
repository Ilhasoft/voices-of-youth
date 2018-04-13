from django import forms

from voicesofyouth.project.models import Project


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64,
                               label="",
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 8px'
                               }))
    password = forms.CharField(max_length=32,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 8px'
                               }),
                               label="")


class DashboardFilterForm(forms.Form):
    project = forms.ModelChoiceField(
        queryset=Project.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control m-b'}))

    def __init__(self, *args, **kwargs):
        available_projects = kwargs.pop('available_projects')
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = available_projects
