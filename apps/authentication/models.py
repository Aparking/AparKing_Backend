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
from apps.payment.enums import MemberId
from apps.authentication.enums import Gender
import stripe

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
    stripe_customer_id = models.CharField(max_length=255,null = True,blank=True)
    stripe_subscription_id = models.CharField(max_length=255, choices=MemberId.choices(), default=MemberId.FREE, blank=True, null=True)
    stripe_credit_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_session_id=models.CharField(max_length=255,null = True)
    code = models.CharField(max_length=10, blank=True,null = True)
    def validate_iban(iban):
        iban = iban.replace(' ','').replace('\t','').replace('\n','')
        
        if len(iban) != 34:
            return False

        iban = iban[4:] + iban[0:4]
        iban = ''.join(str(10 + ord(c) - ord('A')) if c.isalpha() else c for c in iban)
        return int(iban) % 97 == 1
    iban = models.CharField(max_length=34, blank=True, null=True, validators=[validate_iban])


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    
    def get_stripe_id(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Crea una cuenta conectada
        account = stripe.Account.create(
            type='custom',
            country= self.iban[:2].upper(),
            email=self.email,
        )

        # Agrega la cuenta bancaria a la cuenta conectada
        bank_account = stripe.Token.create(
            bank_account={
                'country': self.iban[:2].upper(),
                'currency': 'eur',
                'account_holder_name': self.username,
                'account_holder_type': 'individual',
                'account_number': self.iban,
            },
        )
        
        stripe.Account.create_external_account(
            account['id'],
            external_account=bank_account['id'],
        )
      
        return account['id']

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

class Vehicle(models.Model):
    carModel = models.CharField(max_length=100, blank=False, null=False)
    color = models.CharField(max_length=25, blank=False, null=False)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    length = models.DecimalField(max_digits=6, decimal_places=2)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    principalCar = models.BooleanField(default=True)
    def to_json(self):
        return {
            'id': self.id,
            'carModel': self.carModel,
            'color': self.color,
            'height': str(self.height),
            'width': str(self.width),
            'length': str(self.length),
            'principalCar': self.principalCar
        }
