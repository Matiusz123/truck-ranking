from django import forms
from final.validators import validate_user, validate_password
from django.core.exceptions import ValidationError
from final.models import User


class Signup(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Passwords are not matching")

    def clean_login(self):
        user_name = self.cleaned_data.get('login')
        user = User.objects.filter(username=user_name)
        if user:
            raise ValidationError("User already exits")
        return user_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError("Email already exits")
        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class APIForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) != 10:
            raise ValidationError("Username should be 10 characters")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) != 10:
            raise ValidationError("Password should be 10 characters")
        return password