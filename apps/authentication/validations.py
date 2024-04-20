from stdnum import iban as iban_validator
from django.core.exceptions import ValidationError

def validate_iban(value):
        if not iban_validator.is_valid(value):
            raise ValidationError("Invalid IBAN")