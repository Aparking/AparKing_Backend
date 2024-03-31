import datetime
from decimal import Decimal
from django_countries import countries
from rest_framework import serializers

from apps.authentication.models import CustomUser
from apps.booking.enums import BookingStatus, PaymentMethod
from apps.garagement.enums import GarageStatus
from apps.garagement.models import Availability


def validate_availability_data(availability_data):
    start_date = availability_data.get('start_date', None)
    if not start_date or not isinstance(start_date, datetime.datetime):
        raise serializers.ValidationError("La fecha inicial debe ser una fecha y hora válidas.")

    end_date = availability_data.get('end_date', None)
    if not end_date or not isinstance(end_date, datetime.datetime):
        raise serializers.ValidationError("La fecha final debe ser una fecha y hora válidas.")

    if start_date >= end_date:
        raise serializers.ValidationError("La fecha inicial debe ser anterior a la fecha final.")
    
    if start_date <= datetime.datetime.now():
        raise serializers.ValidationError("La fecha inicial debe ser igual o posterior a la fecha actual.")

    if end_date >= datetime.datetime(2100, 12, 31):
        raise serializers.ValidationError("La fecha final debe ser anterior o igual al 31/12/2100.")

    status = availability_data.get('status', None)
    if not status or status not in [choice[1] for choice in GarageStatus.choices()]:
        valid_statuses = ", ".join([choice[1] for choice in GarageStatus.choices()])
        raise serializers.ValidationError(f"El 'status' debe ser uno de los siguientes valores válidos: {valid_statuses}.")

    return availability_data


def validate_booking_data(book_data):
    payment_method = book_data.get('payment_method', None)
    if not payment_method or payment_method not in [choice[0] for choice in PaymentMethod.choices()]:
        valid_methods = ", ".join([choice[0] for choice in PaymentMethod.choices()])
        raise serializers.ValidationError(f"El método de pago debe ser uno de los siguientes valores válidos: {valid_methods}.")

    status = book_data.get('status', None)
    if not status or status not in [choice[0] for choice in BookingStatus.choices()]:
        valid_statuses = ", ".join([choice[0] for choice in BookingStatus.choices()])
        raise serializers.ValidationError(f"El estado debe ser uno de los siguientes valores válidos: {valid_statuses}.")

    return book_data