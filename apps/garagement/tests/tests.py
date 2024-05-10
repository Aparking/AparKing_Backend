from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
import datetime as dt
from apps.authentication.models import CustomUser
from apps.garagement.enums import GarageStatus
from apps.garagement.models import Address, Garage, Image, Availability

class AddressTestCase(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            street_number='123',
            address_line='Test Street',
            city='Test City',
            region='Test Region',
            country='US',
            postal_code='12345'
        )
    
    def test_create_address(self):
        self.assertEqual(Address.objects.count(), 1)
    
    def test_address_str(self):
        expected_address_string = "123, Test Street, Test City, Test Region, United States of America"
        self.assertEqual(str(self.address), expected_address_string)

class GarageTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com', dni='12345678A',
                                        birth_date=dt.date(1990, 1, 1), gender="M", phone='+123456789')            
        self.address = Address.objects.create(
            street_number='123',
            address_line='Test Street',
            city='Test City',
            region='Test Region',
            country='US',
            postal_code='12345'
        )
        self.garage = Garage.objects.create(
            name='Test Garage',
            description='Test description',
            height=2.5,
            width=5.0,
            length=5.0,
            price=100.00,
            owner=self.user,
            address=self.address
        )
        
    def test_create_garage(self):
        self.assertEqual(Garage.objects.count(), 1)
        
    def test_garage_str(self):
        expected_garage_string = "Test Garage - 123, Test Street, Test City, Test Region, United States of America"
        self.assertEqual(str(self.garage), expected_garage_string)

    def test_garage_clean(self):
        garage = Garage(
            name='Test Garage',
            description='Test description',
            height=2.5,
            width=5.0,
            length=5.0,
            price=-100.00,  # Negative price to test clean method
            owner=self.user,
            address=self.address
        )
        with self.assertRaises(ValidationError):
            garage.full_clean()
            
class ImageTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com', dni='12345678A',
                                        birth_date=dt.date(1990, 1, 1), gender="M", phone='+123456789')            
        self.address = Address.objects.create(
            street_number='123',
            address_line='Test Street',
            city='Test City',
            region='Test Region',
            country='US',
            postal_code='12345'
        )
        self.garage = Garage.objects.create(
            name='Test Garage',
            description='Test description',
            height=2.5,
            width=5.0,
            length=5.0,
            price=100.00,
            owner=self.user,
            address=self.address
        )
        self.image = Image.objects.create(
            image='path/to/image.jpg',
            alt='Test Image',
            garage=self.garage
        )
        
    def test_create_image(self):
        self.assertEqual(Image.objects.count(), 1)

    
    def test_image_str(self):
        expected_image_string = "Test Garage - 123, Test Street, Test City, Test Region, United States of America - Test Image"
        self.assertEqual(str(self.image), expected_image_string)
        
class AvailabilityTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com', dni='12345678A',
                                        birth_date=dt.date(1990, 1, 1), gender="M", phone='+123456789')            
        self.address = Address.objects.create(
            street_number='123',
            address_line='Test Street',
            city='Test City',
            region='Test Region',
            country='US',
            postal_code='12345'
        )
        self.garage = Garage.objects.create(
            name='Test Garage',
            description='Test description',
            height=2.5,
            width=5.0,
            length=5.0,
            price=100.00,
            owner=self.user,
            address=self.address
        )
        self.availability = Availability.objects.create(
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=7),
            status=GarageStatus.AVAILABLE,
            garage=self.garage
        )
        
    def test_create_availability(self):
        self.assertEqual(Availability.objects.count(), 1)
        
    def test_availability_str(self):
        expected_availability_string = "(Disponible) - Garage: Test Garage - 123, Test Street, Test City, Test Region, United States of America"
        self.assertEqual(str(self.availability), expected_availability_string)

    def test_availability_clean(self):
        availability = Availability(
            start_date=datetime.now() + timedelta(days=7),  # End date before start date to test clean method
            end_date=datetime.now(),
            status=GarageStatus.AVAILABLE,
            garage=self.garage
        )
        with self.assertRaises(ValidationError):
            availability.full_clean()