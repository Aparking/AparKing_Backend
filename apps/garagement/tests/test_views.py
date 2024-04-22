from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.garagement.models import Address, Garage
from django_countries.fields import Country
from datetime import date

User = get_user_model()

class GarageAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            birth_date=date(1990, 1, 1)
        )
        self.client.force_authenticate(user=self.user)

        self.address = Address.objects.create(
            street_number="123",
            address_line="Calle Falsa",
            city="Springfield",
            region="Region Test",
            country=Country("US"),
            postal_code="12345"
        )

    def test_create_garage(self):
        url = reverse('garages')
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
                "postal_code": "67890"
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Garage.objects.count(), 1)
