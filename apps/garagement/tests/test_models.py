from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from apps.garagement.models import Garage, Address
from django_countries.fields import Country
from datetime import date

User = get_user_model()

class AddressModelTest(TestCase):
    def test_create_address(self):
        address = Address.objects.create(
            street_number="123",
            address_line="Calle Falsa",
            city="Springfield",
            region="Region Test",
            country=Country("US"),
            postal_code="12345"
        )

        self.assertEqual(str(address), "123, Calle Falsa, Springfield, Region Test, United States of America")

class GarageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword',
            birth_date=date(1990, 1, 1) 
        )
        self.address = Address.objects.create(
            street_number="123",
            address_line="Calle Falsa",
            city="Springfield",
            region="Region Test",
            country=Country("US"),
            postal_code="12345"
        )

    def test_create_garage(self):
        garage = Garage.objects.create(
            name="Garage Test",
            description="Descripción Test",
            height=2.5,
            width=2.5,
            length=5.0,
            price=50.00,
            owner=self.user,
            address=self.address
        )
        self.assertEqual(str(garage), "Garage Test - 123, Calle Falsa, Springfield, Region Test, United States of America")

    def test_garage_price_negative(self):
        with self.assertRaises(ValidationError):
            garage = Garage(
                name="Garage Negative Price",
                description="Descripción Test",
                height=2.5,
                width=2.5,
                length=5.0,
                price=-50.00,
                owner=self.user,
                address=self.address
            )
            garage.full_clean()  # full_clean para validar el modelo antes de guardarlo
