import datetime
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.authentication.models import CustomUser
from django.contrib.auth import get_user_model
from apps.booking.models import Book, Availability
from apps.garagement.models import Garage, Address
from apps.garagement.enums import GarageStatus
from apps.booking.enums import BookingStatus, PaymentMethod
from django_countries.fields import Country


User = get_user_model()

class BookingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            birth_date=datetime.date(1990, 1, 1),
        )
        self.client.force_authenticate(user=self.user)
        self.client.login(username='testuser', password='testpass')
        
        self.adress = Address.objects.create(
            street_number="123",
            address_line="Calle Falsa",
            city="Springfield",
            region="Region Test",
            country=Country("US"),
            postal_code="12345",)
        self.garage = Garage.objects.create(
            name='Test Garage', 
            description='Test description', 
            price=10.0, 
            owner=self.user, 
            height=1.0, 
            width=1.0, 
            length=1.0, 
            address=self.adress, 
            is_active=True, 
            creation_date=now(), 
            modification_date=now())
        self.availability = Availability.objects.create(
            garage=self.garage,
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=datetime.datetime.now() + datetime.timedelta(days=2),
            status=GarageStatus.AVAILABLE.value
        )
        self.booking = Book.objects.create(
            payment_method=PaymentMethod.CARD.value,
            status=BookingStatus.CONFIRMED.value,
            user=self.user,
            availability=self.availability
        )
    
    def test_create_booking(self):
        url = reverse('create_booking')
        data = {
            'availability': self.availability.id,
            'payment_method': PaymentMethod.CARD.value
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], BookingStatus.CONFIRMED.value)

    def test_list_my_bookings(self):
        url = reverse('list_my_bookings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_booking_details_get(self):
        url = reverse('booking_details', args=[self.booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], BookingStatus.CONFIRMED.value)

    def test_booking_details_delete(self):
        url = reverse('booking_details', args=[self.booking.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.booking.id).exists())