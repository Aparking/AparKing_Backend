'''
import datetime
from decimal import Decimal
from django.test import TestCase
from rest_framework import serializers

from apps.authentication.models import CustomUser
from apps.booking.enums import BookingStatus, PaymentMethod
from apps.garagement.enums import GarageStatus
from apps.garagement.models import Availability
from apps.booking.validations import validate_availability_data, validate_booking_data

class ValidateAvailabilityDataTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'start_date': datetime.datetime.now() + datetime.timedelta(days=1),
            'end_date': datetime.datetime.now() + datetime.timedelta(days=2),
            'status': GarageStatus.AVAILABLE.name,
        }

    def test_valid_data(self):
        try:
            validate_availability_data(self.valid_data)
        except serializers.ValidationError:
            self.fail("validate_availability_data() raised ValidationError unexpectedly!")

    def test_missing_start_date(self):
        data = self.valid_data.copy()
        del data['start_date']
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(data)

    def test_invalid_start_date(self):
        data = self.valid_data.copy()
        data['start_date'] = 'not a date'
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(data)

    def test_missing_end_date(self):
        data = self.valid_data.copy()
        del data['end_date']
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(data)

    def test_invalid_end_date(self):
        data = self.valid_data.copy()
        data['end_date'] = 'not a date'
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(data)

    def test_start_date_after_end_date(self):
        data = self.valid_data.copy()
        data['start_date'] = data['end_date'] + datetime.timedelta(days=1)
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(data)

    def test_start_date_in_past(self):
        data = self.valid_data.copy()
        data['start_date'] = datetime.datetime.now() - datetime.timedelta(days=1)
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(data)

    def test_end_date_too_far(self):
        data = self.valid_data.copy()
        data['end_date'] = datetime.datetime(2101, 1, 1)
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(data)

    def test_invalid_status(self):
        data = self.valid_data.copy()
        data['status'] = 'INVALID_STATUS'
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(data)

class ValidateBookingDataTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'payment_method': PaymentMethod.CARD.name,
            'status': BookingStatus.CONFIRMED.name,
        }

    def test_valid_data(self):
        try:
            validate_booking_data(self.valid_data)
        except serializers.ValidationError:
            self.fail("validate_booking_data() raised ValidationError unexpectedly!")

    def test_missing_payment_method(self):
        data = self.valid_data.copy()
        del data['payment_method']
        with self.assertRaises(serializers.ValidationError):
            validate_booking_data(data)

    def test_invalid_payment_method(self):
        data = self.valid_data.copy()
        data['payment_method'] = 'INVALID_METHOD'
        with self.assertRaises(serializers.ValidationError):
            validate_booking_data(data)

    def test_missing_status(self):
        data = self.valid_data.copy()
        del data['status']
        with self.assertRaises(serializers.ValidationError):
            validate_booking_data(data)

    def test_invalid_status(self):
        data = self.valid_data.copy()
        data['status'] = 'INVALID_STATUS'
        with self.assertRaises(serializers.ValidationError):
            validate_booking_data(data)
'''