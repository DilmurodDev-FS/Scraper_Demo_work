from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ScrapeForm(forms.Form):
    url = forms.URLField(
        max_length=1000,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com',
        })
    )

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
