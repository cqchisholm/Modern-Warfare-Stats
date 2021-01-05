from django import forms
from django.forms import fields
from django.forms.models import ModelForm
from .models import Friends, User, Profile
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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label=False, widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': 'autofocus'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class FriendsForm(ModelForm):
    class Meta:
        model = Friends
        fields = ['gamertag1', 'gamertag2', 'gamertag3', 'gamertag4', 'gamertag5']
        widgets = {
            'gamertag1': forms.TextInput(attrs={'placeholder': 'Gamertag 1'}),
            'gamertag2': forms.TextInput(attrs={'placeholder': 'Gamertag 2'}),
            'gamertag3': forms.TextInput(attrs={'placeholder': 'Gamertag 3'}),
            'gamertag4': forms.TextInput(attrs={'placeholder': 'Gamertag 4'}),
            'gamertag5': forms.TextInput(attrs={'placeholder': 'Gamertag 5'})
        }
        labels = {
            'gamertag1': 'Gamertag 1',
            'gamertag2': 'Gamertag 2',
            'gamertag3': 'Gamertag 3',
            'gamertag4': '',
            'gamertag5': ''
        }
