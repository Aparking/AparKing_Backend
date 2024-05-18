from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from apps.authentication.enums import Gender
from apps.authentication.models import CustomUser
from apps.parking.models import City, Parking, Size, ParkingType
from apps.parking.serializers import CitySerializer, ParkingSerializer

class ParkingSerializerTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='password', 
            dni='12345678Z',
            gender=Gender.MALE, 
            phone='+34600000000', 
            birth_date='1990-01-01'
        )
        self.parking = Parking.objects.create(
            location=Point(2.1734, 42.3851, srid=4326),
            size=Size.COMPACTO,
            parking_type=ParkingType.FREE,
            is_assignment=False,
            notified_by=self.user
        )
        self.serializer = ParkingSerializer(instance=self.parking)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'location', 'size', 'parking_type', 'is_assignment', 'notified_by', 'message','cesion_parking','is_transfer','created_at', 'updated_at', 'vehiculo', 'booked_by'])

    def test_location_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['location'], {'latitude': self.parking.location.y, 'longitude': self.parking.location.x})

    def test_notified_by_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['notified_by'], self.user.id)
