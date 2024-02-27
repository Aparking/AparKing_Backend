from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from .enums import Gender

class CustomUser(AbstractUser):
    dni = models.CharField(max_length=9, 
                           unique=True, 
                           blank=False, 
                           null=False,
                           validatos=[
                               RegexValidator(
                                    regex='^\d{8}[a-zA-Z]$',
                                    message='Introducza un DNI válido',
                                    code='invalid_dni'
                               )
                           ])
    birth_date = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=1, choices=Gender.choices())
    phone = PhoneNumberField(blank=False, null=False)
