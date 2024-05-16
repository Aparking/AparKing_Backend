from datetime import date, timedelta
import datetime
from django.test import TestCase
from apps.authentication.enums import Gender
from apps.authentication.models import CustomUser
from apps.garagement.enums import GarageStatus
from apps.garagement.models import Address, Availability, Garage
from apps.garagement.serializers import AddressSerializer, AvailabilitySerializer, GarageSerializer, ImageSerializer
from django_countries.fields import Country
from phonenumber_field.phonenumber import PhoneNumber
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PilImage

class AddressSerializerTest(TestCase):
    def test_valid_serializer(self):
        valid_serializer_data = {
            "street_number": "123",
            "address_line": "Calle Falsa",
            "city": "Springfield",
            "region": "Region Test",
            "country": "US",
            "postal_code": "12345"
        }
        serializer = AddressSerializer(data=valid_serializer_data)
        self.assertTrue(serializer.is_valid())
        address = serializer.save()
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(str(address), "123, Calle Falsa, Springfield, Region Test, United States of America")

class ImageSerializerTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            street_number="123",
            address_line="Test Street",
            city="Test City",
            region="Test Region",
            country="ES",
            postal_code="12345"
        )
        self.owner = CustomUser.objects.create(
            username="Test User",
            email="testuser@example.com",
            dni="12345678Z",
            birth_date=date.today(),
            gender=Gender.MALE,
            phone=PhoneNumber.from_string(phone_number="+34123456789", region="ES")
        )
        self.garage = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=2.5,
            width=2.5,
            length=5.0,
            price=100.0,
            owner=self.owner,
            address=self.address
        )

        # Create a test image
        image = PilImage.new("RGB", (100, 100))
        image_file = BytesIO()
        image.save(image_file, "JPEG")
        image_file.seek(0)

        self.image = SimpleUploadedFile("test_image.jpg", image_file.read(), content_type="image/jpeg")

    def test_valid_serializer(self):
        valid_serializer_data = {
            "garage": self.garage.id,
            "image": self.image,
            "alt": "Test Image",
        }
        serializer = ImageSerializer(data=valid_serializer_data)
        valid = serializer.is_valid()
        if not valid:
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        image = serializer.save()
        self.assertEqual(image.garage, self.garage)
        self.assertEqual(image.alt, "Test Image")

class GarageSerializerTestCase(TestCase):
    def setUp(self):
        self.owner = CustomUser.objects.create(
            username="Test User",
            email="testuser@example.com",
            dni="12345678Z",
            birth_date=date.today(),
            gender=Gender.MALE,
            phone=PhoneNumber.from_string(phone_number="+34123456789", region="ES")
        )
        self.address = Address.objects.create(
            street_number="123",
            address_line="Test Street",
            city="Test City",
            region="Test Region",
            country="ES",
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=2.5,
            width=2.5,
            length=5.0,
            price=100.0,
            owner=self.owner,
            address=self.address
        )
        self.serializer = GarageSerializer(instance=self.garage)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'height', 'width', 'length', 'price', 'creation_date', 'modification_date', 'is_active', 'owner', 'address'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.garage.name)

    def test_is_active_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['is_active'], self.garage.is_active)

class AvailabilitySerializerTestCase(TestCase):
    def setUp(self):
        self.owner = CustomUser.objects.create(
            username="Test User",
            email="testuser@example.com",
            dni="12345678Z",
            birth_date=date.today(),
            gender=Gender.MALE,
            phone=PhoneNumber.from_string(phone_number="+34123456789", region="ES")
        )
        self.address = Address.objects.create(
            street_number="123",
            address_line="Test Street",
            city="Test City",
            region="Test Region",
            country="ES",
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=2.5,
            width=2.5,
            length=5.0,
            price=100.0,
            owner=self.owner,
            address=self.address
        )
        self.availability = Availability.objects.create(
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            status=GarageStatus.AVAILABLE,
            garage=self.garage
        )
        self.serializer = AvailabilitySerializer(instance=self.availability)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'start_date', 'end_date', 'status', 'garage'])

    def test_garage_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['garage'], self.garage.id)

    def test_status_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['status'], self.availability.status)