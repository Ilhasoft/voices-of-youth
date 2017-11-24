from django import forms


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
