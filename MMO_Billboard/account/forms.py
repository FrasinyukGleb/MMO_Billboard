from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
