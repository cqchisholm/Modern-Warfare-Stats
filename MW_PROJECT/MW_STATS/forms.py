from django import forms
from django.forms import fields
from django.forms.models import ModelForm
from .models import Friends, User, Profile
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

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
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'
        # the below doesn't work too well
        self.helper.layout = Layout(
            Field('gamertag1', css_class='form-divide'),
            Field('gamertag2', css_class='form-divide'),
            Field('gamertag3', css_class='form-divide'),
            Field('gamertag4', css_class='form-divide'),
            Field('gamertag5', css_class='form-divide')
        )
        self.helper.add_input(Submit('submit', 'Add Friends'))
        super(FriendsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Friends
        fields = ['gamertag1', 'gamertag2', 'gamertag3', 'gamertag4', 'gamertag5']
        labels = {
            'gamertag1': 'Gamertag 1',
            'gamertag2': 'Gamertag 2',
            'gamertag3': 'Gamertag 3',
            'gamertag4': 'Gamertag 4',
            'gamertag5': 'Gamertag 5'
        }
        widgets = {
            'gamertag1': forms.TextInput(attrs={
                'autofocus': 'autofocus'
            })
        }
