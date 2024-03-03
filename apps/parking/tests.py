from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework.test import APITestCase
from apps.authentication.models import CustomUser

class ParkingTestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = CustomUser.objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='password', 
            dni='12345678Z', 
            phone='+34600000000', 
            birth_date='1990-01-01'
        )
        
        self.client.login(email='testuser@example.com', password='password')
        self.create_parking_url = reverse('create_parking')

    def tearDown(self):
        super().tearDown()

    def test_create_parking_success(self):
        data = {
            "location": {
                "type": "Point",
                "coordinates": [42.3851,2.1734]
            },
            "size": "SMALL",
            "parking_type": "FREE",
        }
        
        response = self.client.post(self.create_parking_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.json())