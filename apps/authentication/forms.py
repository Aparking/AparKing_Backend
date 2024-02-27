from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from .models import BaseUser, AparkingUser

class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', required=True)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(), required=True)

class RegisterForm(forms.Form):
    name = forms.CharField(label='Nombre Completo', required=True)
    email = forms.EmailField(label='Correo Electrónico', required=True)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(), required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = get_user_model().objects.filter(email=email)
        if qs.exists():
            self.add_error('email', 'El correo electrónico ya está registrado')
        try:
            validate_email(email)
        except:
            self.add_error('email', 'El correo electrónico no es válido')
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            self.add_error('password', 'La contraseña debe tener al menos 8 caracteres')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
    
    
    def save(self, commit=True):
        user = get_user_model().objects.create_user(
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
        )
        return user