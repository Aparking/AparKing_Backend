from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from .enums import Gender

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

from apps.authentication.enums import Gender


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=False, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    dni = models.CharField(max_length=9, 
                           unique=True, 
                           blank=False, 
                           null=False,
                           validators=[
                               RegexValidator(
                                    regex='^\d{8}[a-zA-Z]$',
                                    message='Introduzca un DNI válido',
                                    code='invalid_dni'
                               )
                           ])
    birth_date = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=16, choices=Gender.choices())
    photo = models.URLField(blank=True, null=True)
    phone = PhoneNumberField(blank=False, null=False)
    code = models.CharField(max_length=10, blank=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

class Vehicle(models.Model):
    carModel = models.CharField(max_length=100, blank=False, null=False)
    color = models.CharField(max_length=25, blank=False, null=False)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    length = models.DecimalField(max_digits=6, decimal_places=2)
