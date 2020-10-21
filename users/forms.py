from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label=('Nom utilisateur'))
    email = forms.EmailField()
    last_name = forms.CharField(label=("Nom"), required=True)
    first_name = forms.CharField(label=("Prenom"), required=True)
    password1 = forms.CharField(label=("Mot de passe"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Confirmez votre mot de passe"),
                                widget=forms.PasswordInput,

                                help_text=("Même mot de passe que avant."))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Un compte est déjà associé à cet email')
        return email

    class Meta:
        #  Here we say that the model that will be affected by our form is User
        #  And then the fields that we want in our form and in what order
        model = User
        fields = ['username', 'email', 'last_name', 'first_name',
                  'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(label=('Nom utilisateur'))
    password = forms.CharField(label=("Mot de passe"),
                               widget=forms.PasswordInput)
    last_name = forms.CharField(label=("Nom"))
    first_name = forms.CharField(label=("Prenom"))


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']

class ProfileUpdateForme(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']