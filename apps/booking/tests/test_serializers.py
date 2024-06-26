from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from apps.booking.serializers import AvailabilitySerializer, CommentSerializer
from phonenumber_field.phonenumber import PhoneNumber
from apps.authentication.enums import Gender
from apps.authentication.models import CustomUser
from apps.booking.enums import BookingStatus, PaymentMethod
from apps.booking.models import Book, Comment
from apps.booking.serializers import BookSerializer
from apps.garagement.enums import GarageStatus
from apps.garagement.models import Address, Availability, Garage
from datetime import datetime, timedelta
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token

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

class CommentSerializerTestCase(TestCase):
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
        self.comment = Comment.objects.create(
            title="Test Comment",
            description="Test Description",
            publication_date=datetime.now(),
            rating=5,
            user=self.owner,
            garage=self.garage
        )
        self.serializer = CommentSerializer(instance=self.comment)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'title', 'description', 'publication_date', 'rating', 'user', 'garage'])

    def test_garage_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['garage'], self.garage.id)

    def test_user_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['user'], self.owner.id)

class BookSerializerTestCase(TestCase):
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
        self.book = Book.objects.create(
            payment_method=PaymentMethod.CARD,
            status=BookingStatus.PENDING,
            user=self.owner,
            availability=self.availability,
            stripe_session_id="test_stripe_session_id"
        )
        self.serializer = BookSerializer(instance=self.book)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'payment_method', 'status', 'user', 'availability', 'stripe_session_id'])

    def test_availability_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['availability'], self.availability.id)

    def test_status_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['status'], self.book.status)