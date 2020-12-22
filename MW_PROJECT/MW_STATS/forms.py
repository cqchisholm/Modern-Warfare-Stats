from django import forms
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    # Need to enter info for each field so I can override the defaults (labels, help-text, etc.)
    gamertag = forms.CharField(max_length=30, label=False, widget=forms.TextInput(attrs={'placeholder': 'Gamertag', 'autofocus': 'autofocus'}))
    username = forms.CharField(max_length=30, label=False, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(max_length=30, label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=30, label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Verify Password'}))

    class Meta:
        model = User
        fields = ('gamertag', 'username', 'password1', 'password2', )
        