from django import forms
from final.validators import validate_user, validate_password
from django.core.exceptions import ValidationError
from final.models import User


class Signup(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-container submit', 'placeholder': 'Username'}),
        validators=[validate_user],
        label='')
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-container submit', 'placeholder': 'Email'}),
        label='')
    company_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-container submit', 'placeholder': 'Company name (optional)'}),
        validators=[validate_user],
        label='',
        required=False)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-container submit', 'placeholder': 'Password'}),
        validators=[validate_password],
        label='')

    def clean_login(self):
        user_name = self.cleaned_data.get('login')
        user_email = self.cleaned_data.get('email')
        user = User.objects.filter(username=user_name, email=user_email)
        if user:
            raise ValidationError("Podana nazwa użytkownika lub email jest już zarezerwowana")

        return user_name
