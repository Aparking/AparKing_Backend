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
        
class GarageListViewTest(APITestCase):
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
        self.address = Address.objects.create(
            street_number="123",
            address_line="Fake Street",
            city="Testville",
            region="Test Region",
            country="US",
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
        self.client.login(username='testuser', password='testpass')
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
        
    def test_list_garages_as_admin(self):
        self.client.login(username='admin', password='admin')
        self.client.force_authenticate(user=self.admin)
        url = reverse('garages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_garages_as_normal_user(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('garages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Garage')