import datetime
from decimal import Decimal
from django_countries import countries
from rest_framework import serializers

from apps.garagement.enums import GarageStatus

def validate_address_data(address_data):
    street_number = address_data.get('street_number', None)
    if not street_number or not isinstance(street_number, str) or len(street_number) > 8:
        raise serializers.ValidationError("El número de calle debe ser una cadena no vacía de máximo 8 caracteres.")

    unit_number = address_data.get('unit_number', None)
    if unit_number and (not isinstance(unit_number, str) or len(unit_number) > 8):
        raise serializers.ValidationError("El número de unidad, si se proporciona, debe ser una cadena de máximo 8 caracteres.")

    address_line = address_data.get('address_line', None)
    if not address_line or not isinstance(address_line, str):
        raise serializers.ValidationError("La línea de dirección debe ser una cadena no vacía.")

    city = address_data.get('city', None)
    if not city or not isinstance(city, str) or len(city) > 256:
        raise serializers.ValidationError("La ciudad debe ser una cadena no vacía de máximo 256 caracteres.")

    region = address_data.get('region', None)
    if not region or not isinstance(region, str) or len(region) > 256:
        raise serializers.ValidationError("La región debe ser una cadena no vacía de máximo 256 caracteres.")

    country = address_data.get('country', None)
    if not country or country not in dict(countries):
        raise serializers.ValidationError("El país debe ser un código de país válido.")

    postal_code = address_data.get('postal_code', None)
    if not postal_code or not isinstance(postal_code, str) or len(postal_code) > 16:
        raise serializers.ValidationError("El código postal debe ser una cadena no vacía de máximo 16 caracteres.")

    return address_data


def validate_garage_data(garage_data):
    name = garage_data.get('name', None)
    if not name or not isinstance(name, str) or len(name) > 256:
        raise serializers.ValidationError("El nombre debe ser una cadena no vacía de máximo 256 caracteres.")

    description = garage_data.get('description', None)
    if not description or not isinstance(description, str) or len(description) > 1024:
        raise serializers.ValidationError("La descripción debe ser una cadena no vacía de máximo 1024 caracteres.")

    for dimension in ['height', 'width', 'length']:
        if dimension in garage_data:
            value = garage_data[dimension]
            if not isinstance(value, Decimal) or value <= 0:
                raise serializers.ValidationError(f"La {dimension} debe ser un número decimal positivo.")

    price = garage_data.get('price', None)
    if price is not None:
        if not isinstance(price, Decimal) or price < 0:
            raise serializers.ValidationError("El precio debe ser un valor decimal no negativo.")
    
    is_active = garage_data.get('is_active', None)
    if not isinstance(is_active, bool):
        raise serializers.ValidationError("is_active debe ser un valor booleano.")

    return garage_data


def validate_image_data(image_data):
    image = image_data.get('image', None)
    if not image:
        raise serializers.ValidationError("El campo 'image' es obligatorio.")

    alt = image_data.get('alt', None)
    if not alt or not isinstance(alt, str) or len(alt) > 256:
        raise serializers.ValidationError("El campo 'alt' debe ser una cadena no vacía de máximo 256 caracteres.")

    return image_data


def validate_availability_data(availability_data):
    start_date = availability_data.get('start_date', None)
    if not start_date or not isinstance(start_date, datetime.datetime):
        raise serializers.ValidationError("La 'start_date' debe ser una fecha y hora válidas.")

    end_date = availability_data.get('end_date', None)
    if not end_date or not isinstance(end_date, datetime.datetime):
        raise serializers.ValidationError("La 'end_date' debe ser una fecha y hora válidas.")

    if start_date >= end_date:
        raise serializers.ValidationError("La 'start_date' debe ser anterior a la 'end_date'.")

    status = availability_data.get('status', None)
    if not status or status not in [choice.value for choice in GarageStatus.choices()]:
        valid_statuses = ", ".join([choice.value for choice in GarageStatus.choices()])
        raise serializers.ValidationError(f"El 'status' debe ser uno de los siguientes valores válidos: {valid_statuses}.")

    return availability_data
