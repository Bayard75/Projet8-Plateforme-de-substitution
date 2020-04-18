from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label=('Nom utilisateur'))
    email =forms.EmailField()
    password1 = forms.CharField(label=("Mot de passe"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Confirmez votre mot de passe"),
        widget=forms.PasswordInput,
        help_text=("Tappez le même mot de passe que précedement."))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Un compte est déjà associé à cet email')
        return email

    class Meta:
    # Here we say that the model that will be affected by our form is User
    # And then the fields that we want in our form and in what order
        model = User
        fields = ['username','email','password1','password2']

class LoginForm(forms.Form):
    username = forms.CharField(label=('Nom utilisateur'))
    password = forms.CharField(label=("Mot de passe"), widget=forms.PasswordInput)
    
