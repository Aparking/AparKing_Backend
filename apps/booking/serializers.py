from apps.authentication.models import CustomUser
from apps.booking.enums import BookingStatus, PaymentMethod
from apps.booking.models import Book
from apps.garagement.enums import GarageStatus
from apps.garagement.models import Availability, Garage
from apps.garagement.serializers import AvailabilitySerializer, GarageSerializer
from rest_framework import serializers

from . import validations
from .models import Comment


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

    def validate(self, attrs):
        return validations.validate_availability_data(attrs)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['payment_method', 'status', 'user', 'availability']

    def validate(self, attrs):
        return validations.validate_booking_data(attrs)

    def create(self, validated_data):
        availability = validated_data.pop('availability')
        booking = Book.objects.create(availability=availability, **validated_data)
        return booking


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, attrs):
        return attrs
