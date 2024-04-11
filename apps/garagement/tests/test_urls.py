from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.garagement.models import Address, Garage
from django_countries.fields import Country
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
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

        self.garage = Garage.objects.create(
            name="Setup Garage",
            description="Setup Description",
            height=2.5,
            width=2.5,
            length=5.0,
            price=50.00,
            owner=self.user,
            address=self.address,
            is_active=True
        )

        # Create a test image
        image = Image.new('RGB', (100, 100))
        image_file = BytesIO()
        image.save(image_file, 'JPEG')
        image_file.seek(0)

        self.image = SimpleUploadedFile("test_image.jpg", image_file.read(), content_type="image/jpeg")
'''
    def test_create_garage(self):
        url = reverse('garages')
        data = {
            "name": "Test Garage",
            "description": "Test Description",
            "height": 3.0,
            "width": 3.0,
            "length": 6.0,
            "price": 100.00,
            "is_active": True,
            "owner": self.user.id,
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
'''