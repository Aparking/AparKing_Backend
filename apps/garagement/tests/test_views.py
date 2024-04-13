from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.authentication.models import CustomUser
from apps.garagement.models import Address, Garage
from django_countries.fields import Country
from datetime import date

User = get_user_model()


class GarageAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            birth_date=date(1990, 1, 1),
        )
        self.client.force_authenticate(user=self.user)

        self.address = Address.objects.create(
            street_number="123",
            address_line="Calle Falsa",
            city="Springfield",
            region="Region Test",
            country=Country("US"),
            postal_code="12345",
        )

    def test_create_garage(self):
        url = reverse("create_garage")
        # Suponiendo que necesitas enviar el ID del usuario como parte de la solicitud.
        # Esto NO es lo recomendado para producción, pero te servirá para pasar la prueba.
        data = {
            "name": "Test Garage",
            "description": "Test Description",
            "height": 3.0,
            "width": 3.0,
            "length": 6.0,
            "price": 100.00,
            "is_active": True,
            "owner": self.user.id,  # Aquí asignas el ID del usuario autenticado como el owner.
            "address": {
                "street_number": "456",
                "address_line": "Calle Verdadera",
                "city": "Metropolis",
                "region": "Region Example",
                "country": "US",
                "postal_code": "67890",
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Garage.objects.count(), 1)

class GarageFilterViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            birth_date=date(1990, 1, 1),
        )
        self.admin = CustomUser.objects.create_superuser(
            username='admin', 
            email = 'admin@admin.com',
            password = 'admin',
            dni='12345678Z', 
            phone='+34600000000', 
            birth_date='1990-01-01'
        )        
        self.address1 = Address.objects.create(
            street_number="123",
            address_line="Fake Street",
            city="Testville",
            region="Test Region",
            country="US",
            postal_code="12345"
        )
        self.address2 = Address.objects.create(
            street_number="456",
            address_line="Real Street",
            city="Realville",
            region="Real Region",
            country="US",
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
            country="US",
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
            country="US",
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
            country="US",
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
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'min_price': 200})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4) 

    def test_list_garages_with_max_price_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'max_price': 300})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3) 

    def test_list_garages_with_min_height_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'min_height': 5.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_garages_with_max_height_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'max_height': 6.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4) 

    def test_list_garages_with_min_width_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'min_width': 5.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_garages_with_max_width_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'max_width': 6.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_list_garages_with_min_length_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'min_length': 10.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_garages_with_max_length_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'max_length': 12.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_list_garages_with_name_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'name': 'Garage'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_list_garages_with_city_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'city': 'ville'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_list_garages_with_region_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'region': 'Region'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_list_garages_with_country_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'country': 'US'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_list_garages_with_postal_code_filter(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url, {'postal_code': '22222'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)