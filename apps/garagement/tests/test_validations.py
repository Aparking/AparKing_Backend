import datetime
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.booking.validations import validate_availability_data
from apps.garagement.enums import GarageStatus
from apps.garagement.models import Address
from rest_framework import serializers
from django_countries import countries
from apps.garagement.validations import validate_address_data, validate_garage_data, validate_image_data
from django_countries.fields import Country


class ValidateAddressDataTests(TestCase):
    def test_valid_address_data(self):
        adress_data = {
            "street_number": "123",
            "address_line": "Fake Street",
            "city": "Testville",
            "region": "Test Region",
            "country": Country("US"),
            "postal_code": "12345"
        }
        validated_data = validate_address_data(adress_data)
        self.assertEqual(validated_data, adress_data)

    def test_invalid_street_number(self):
        address_data = {"street_number": "123"}
        with self.assertRaises(serializers.ValidationError):
            validate_address_data(address_data)

    def test_invalid_city(self):
        address_data = {"city": "C" * 257}
        with self.assertRaises(serializers.ValidationError):
            validate_address_data(address_data)

    def test_invalid_country(self):
        address_data = {"country": "XX"}
        with self.assertRaises(serializers.ValidationError):
            validate_address_data(address_data)

    def test_invalid_postal_code(self):
        address_data = {"postal_code": "X" * 17}
        with self.assertRaises(serializers.ValidationError):
            validate_address_data(address_data)
            
class ValidateGarageDataTests(TestCase):

    def test_valid_garage_data(self):
        garage_data = {
            "name": "Garage",
            "description": "Descripción del garage",
            "height": Decimal("2.5"),
            "width": Decimal("2.0"),
            "length": Decimal("5.0"),
            "price": Decimal("100.0"),
            "is_active": True
        }
        validated_data = validate_garage_data(garage_data)
        self.assertEqual(validated_data, garage_data)

    def test_invalid_name(self):
        garage_data = {"name": ""}
        with self.assertRaises(serializers.ValidationError):
            validate_garage_data(garage_data)

    def test_invalid_height(self):
        garage_data = {"height": Decimal("-1.0")}
        with self.assertRaises(serializers.ValidationError):
            validate_garage_data(garage_data)

    def test_invalid_price(self):
        garage_data = {"price": Decimal("-1.0")}
        with self.assertRaises(serializers.ValidationError):
            validate_garage_data(garage_data)

    def test_invalid_is_active(self):
        garage_data = {"is_active": "yes"}
        with self.assertRaises(serializers.ValidationError):
            validate_garage_data(garage_data)
            
class ValidateImageDataTests(TestCase):

    def test_valid_image_data(self):
        image_data = {
            "image": "\images\test_images_garagement\garaje_test.jpg",
            "alt": "Descripción de la imagen"
        }
        validated_data = validate_image_data(image_data)
        self.assertEqual(validated_data, image_data)

    def test_missing_image(self):
        image_data = {"alt": "Descripción de la imagen"}
        with self.assertRaises(serializers.ValidationError):
            validate_image_data(image_data)

    def test_invalid_alt(self):
        image_data = {"image": "\images\test_images_garagement\garaje_test.jpg", "alt": ""}
        with self.assertRaises(serializers.ValidationError):
            validate_image_data(image_data)

class ValidateAvailabilityDataTests(TestCase):

    def test_valid_availability_data(self):
        availability_data = {
            "start_date":datetime.datetime.now() + datetime.timedelta(days=1),
            "end_date": datetime.datetime.now() + datetime.timedelta(days=2),
            "status": GarageStatus.AVAILABLE.value
        }
        validated_data = validate_availability_data(availability_data)
        self.assertEqual(validated_data, availability_data)

    def test_invalid_start_date(self):
        availability_data = {"start_date": "invalid date"}
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(availability_data)

    def test_invalid_end_date(self):
        availability_data = {
            "start_date": datetime.datetime(2024, 5, 18, 10, 0),
            "end_date": "invalid date"
        }
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(availability_data)

    def test_end_date_before_start_date(self):
        availability_data = {
            "start_date": datetime.datetime(2024, 5, 18, 12, 0),
            "end_date": datetime.datetime(2024, 5, 18, 10, 0)
        }
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(availability_data)

    def test_invalid_status(self):
        availability_data = {
            "start_date": datetime.datetime(2024, 5, 18, 10, 0),
            "end_date": datetime.datetime(2024, 5, 18, 12, 0),
            "status": "invalid status"
        }
        with self.assertRaises(serializers.ValidationError):
            validate_availability_data(availability_data)