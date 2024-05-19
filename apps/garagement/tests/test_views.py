import datetime
from decimal import Decimal
from django.urls import reverse
from apps.garagement.enums import GarageStatus
from apps.garagement.serializers import AvailabilitySerializer, GarageSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.authentication.models import CustomUser
from apps.garagement.models import Address, Availability, Garage
from django_countries.fields import Country
from datetime import date

User = get_user_model()

class GarageListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            birth_date=date(1990, 1, 1),
        )
        self.client.force_authenticate(user=self.user)
        self.client.login( username='testuser', password='testpass')
        
        self.address = Address.objects.create(
            street_number="123",
            address_line="Fake Street",
            city="Testville",
            region="Test Region",
            country=Country("US"),
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=3.0,
            width=3.0,
            length=6.0,
            price=100.00,
            is_active=True,
            owner=self.user,
            address=self.address
        )
        self.garage_not_active = Garage.objects.create(
            name="Test Garage 2",
            description="Test Description 2",
            height=4.0,
            width=4.0,
            length=7.0,
            price=150.00,
            is_active=False,
            owner=self.user,
            address=self.address
        )

    def test_list_garages(self):
        url = reverse('garages') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Garage')

    def test_list_garages_no_results(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'min_price': 200})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_garages_as_normal_user(self):
        url = reverse('garages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Garage')


class GarageFilterViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            birth_date=date(1990, 1, 1),
        )
        self.client.force_authenticate(user=self.user)
        self.client.login( username='testuser', password='testpass')
      
        self.address1 = Address.objects.create(
            street_number="123",
            address_line="Fake Street",
            city="Testville",
            region="Test Region",
            country=Country("US"),
            postal_code="12345"
        )
        self.address2 = Address.objects.create(
            street_number="456",
            address_line="Real Street",
            city="Realville",
            region="Real Region",
            country=Country("US"),
            postal_code="67890"
        )
        self.garage1 = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=3.0,
            width=3.0,
            length=6.0,
            price=100.00,
            is_active=True,
            owner=self.user,
            address=self.address1
        )
        self.garage2 = Garage.objects.create(
            name="Real Garage",
            description="Real Description",
            height=4.0,
            width=4.0,
            length=8.0,
            price=200.00,
            is_active=True,
            owner=self.user,
            address=self.address2
        )
        self.address3 = Address.objects.create(
            street_number="789",
            address_line="Imaginary Street",
            city="Imaginaryville",
            region="Imaginary Region",
             country=Country("US"),
            postal_code="11111"
        )
        self.garage3 = Garage.objects.create(
            name="Imaginary Garage",
            description="Imaginary Description",
            height=5.0,
            width=5.0,
            length=10.0,
            price=300.00,
            is_active=True,
            owner=self.user,
            address=self.address3
        )

        self.address4 = Address.objects.create(
            street_number="012",
            address_line="Fictional Street",
            city="Fictionville",
            region="Fiction Region",
            country=Country("US"),
            postal_code="22222"
        )
        self.garage4 = Garage.objects.create(
            name="Fictional Garage",
            description="Fictional Description",
            height=6.0,
            width=6.0,
            length=12.0,
            price=400.00,
            is_active=True,
            owner=self.user,
            address=self.address4
        )

        self.address5 = Address.objects.create(
            street_number="345",
            address_line="Nonexistent Street",
            city="Nonexistentville",
            region="Nonexistent Region",
            country=Country("US"),
            postal_code="33333"
        )
        self.garage5 = Garage.objects.create(
            name="Nonexistent Garage",
            description="Nonexistent Description",
            height=7.0,
            width=7.0,
            length=14.0,
            price=500.00,
            is_active=True,
            owner=self.user,
            address=self.address5
        )

    def test_list_garages_with_min_price_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'min_price': 200})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4) 

    def test_list_garages_with_max_price_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'max_price': 300})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3) 

    def test_list_garages_with_min_height_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'min_height': 5.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_garages_with_max_height_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'max_height': 6.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4) 

    def test_list_garages_with_min_width_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'min_width': 5.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_garages_with_max_width_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'max_width': 6.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_list_garages_with_min_length_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'min_length': 10.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_garages_with_max_length_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'max_length': 12.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_list_garages_with_name_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'name': 'Garage'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_list_garages_with_city_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'city': 'ville'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_list_garages_with_region_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'region': 'Region'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_list_garages_with_country_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'country': 'US'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_list_garages_with_postal_code_filter(self):
        url = reverse('garages')
        response = self.client.get(url, {'postal_code': '22222'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ListMyGaragesTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            birth_date=date(1990, 1, 1),
        )
        self.client.force_authenticate(user=self.user)
        self.client.login( username='testuser', password='testpass')
        
        self.address = Address.objects.create(
            street_number="123",
            address_line="Fake Street",
            city="Testville",
            region="Test Region",
             country=Country("US"),
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=3.0,
            width=3.0,
            length=6.0,
            price=100.00,
            is_active=True,
            owner=self.user,
            address=self.address
        )
        
    def test_list_my_garages(self):
        url = reverse('my_garages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_no_garages_found(self):
        self.garage.delete()
        url = reverse('my_garages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GarageDetailTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            birth_date=date(1990, 1, 1),
        )
        self.client.force_authenticate(user=self.user)
        self.client.login( username='testuser', password='testpass')
        self.address = Address.objects.create(
            street_number="123",
            address_line="Fake Street",
            city="Testville",
            region="Test Region",
             country=Country("US"),
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=3.0,
            width=3.0,
            length=6.0,
            price=100.00,
            is_active=True,
            owner=self.user,
            address=self.address
        )

    def test_get_garage(self):
        url = reverse('garage', args=[self.garage.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, GarageSerializer(self.garage).data)

    '''
    def test_update_garage(self):
        self.url = reverse('garage', args=[self.garage.id])
        self.data = {'name': 'Updated Garage', 'price': 150.0}
        response = self.client.put(self.url, self.data, format='json')
        self.garage.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.garage.name, 'Updated Garage')
        self.assertEqual(self.garage.price, 150)
    '''

    def test_delete_garage(self):
        url = reverse('garage', args=[self.garage.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Garage.objects.filter(id=self.garage.id).exists())

    def test_garage_not_found(self):
        url = reverse('garage', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class CreateGarageTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            birth_date=date(1990, 1, 1),
        )
        self.client.force_authenticate(user=self.user)
        self.client.login( username='testuser', password='testpass')
        self.address = Address.objects.create(
            street_number="123",
            address_line="Fake Street",
            city="Testville",
            region="Test Region",
             country=Country("US"),
            postal_code="12345"
        )

    '''
    def test_create_garage(self):
        url = reverse('create_garage')
        data = {'owner': self.user.id, 'name': 'New Garage', 'price': 200.0, 
                'description': 'New Description', 'height': 4.0, 'width': 4.0, 'length': 8.0, 
                'is_active': True, 'address': self.address.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Garage.objects.count(), 1)
        self.assertEqual(Garage.objects.get().name, 'New Garage')
    '''

    def test_create_garage_invalid_data(self):
        url = reverse('create_garage')
        data = {'name': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class AvailabilityDetailTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            birth_date=date(1990, 1, 1),
        )
        self.client.force_authenticate(user=self.user)
        self.client.login( username='testuser', password='testpass')
        self.address = Address.objects.create(
            street_number="123",
            address_line="Fake Street",
            city="Testville",
            region="Test Region",
             country=Country("US"),
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=3.0,
            width=3.0,
            length=6.0,
            price=100.00,
            is_active=True,
            owner=self.user,
            address=self.address
        )
        self.availability = Availability.objects.create(
            garage=self.garage,
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=datetime.datetime.now() + datetime.timedelta(days=2),
            status=GarageStatus.AVAILABLE.value
        )

    def test_get_availability(self):
        url = reverse('get_availabilities_by_garage_id', args=[self.availability.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_availability(self):
        url = reverse('update_availability', args=[self.availability.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Availability.objects.filter(id=self.availability.id).exists())

    def test_availability_not_found(self):
        url = reverse('get_availabilities_by_garage_id', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateAvailabilityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            birth_date=date(1990, 1, 1),
        )
        self.client.force_authenticate(user=self.user)
        self.client.login( username='testuser', password='testpass')
        self.address = Address.objects.create(
            street_number="123",
            address_line="Fake Street",
            city="Testville",
            region="Test Region",
             country=Country("US"),
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=3.0,
            width=3.0,
            length=6.0,
            price=100.00,
            is_active=True,
            owner=self.user,
            address=self.address
        )

    '''
    def test_create_availability(self):
        url = reverse('create_availability')
        data = {'garage': self.garage.id, 'start_date': datetime.datetime.now() + datetime.timedelta(days=1),
                'end_date': datetime.datetime.now() + datetime.timedelta(days=2), 'status': GarageStatus.AVAILABLE.value}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Availability.objects.count(), 1)
        self.assertEqual(Availability.objects.get().start_date, datetime.datetime.now() + datetime.timedelta(days=1))
    '''

    def test_create_availability_invalid_data(self):
        url = reverse('create_availability')
        data = {'stat_date': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ListAvailabilitiesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            birth_date=date(1990, 1, 1),
        )
        self.client.force_authenticate(user=self.user)
        self.client.login( username='testuser', password='testpass')
        self.address = Address.objects.create(
            street_number="123",
            address_line="Fake Street",
            city="Testville",
            region="Test Region",
             country=Country("US"),
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=3.0,
            width=3.0,
            length=6.0,
            price=100.00,
            is_active=True,
            owner=self.user,
            address=self.address
        )
        self.availability = Availability.objects.create(
            garage=self.garage,
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=datetime.datetime.now() + datetime.timedelta(days=2),
            status=GarageStatus.AVAILABLE.value
        )

    def test_list_availabilities(self):
        url = reverse('list_availabilities')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


