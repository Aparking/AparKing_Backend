from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework.test import APITestCase
from apps.authentication.models import CustomUser
from apps.parking.models import City, Parking, Size, ParkingType


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
        
        url_login = reverse('login')
        # Primero, inicia sesión
        data = {'password': 'password', 'email': 'testuser@example.com'}
        response = self.client.post(url_login, data, format='json')
        # Luego, prueba el logout
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.create_parking_url = reverse('create_parking')

    def tearDown(self):
        super().tearDown()

    def test_create_parking_success(self):
        data = {
            "latitude":"42.3851",
            "longitude":"2.2734",
            "size": "COMPACTO",
            "parking_type": "FREE",
        }
        
        response = self.client.post(self.create_parking_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.json())
    
    def test_assign_parking_success(self):
        parking = Parking.objects.create(
            location=Point(2.1734, 42.3851, srid=4326),
            size=Size.COMPACTO,
            parking_type=ParkingType.FREE,
            is_assignment=False,
            notified_by=self.user
        )
        assign_parking_url = reverse('assign_parking', kwargs={'parking_id': parking.id})
        
        response = self.client.put(assign_parking_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Parking assigned", response.json()["message"])

    def test_transfer_parking_success(self):
        parking = Parking.objects.create(
            location=Point(2.1734, 42.3851, srid=4326),
            size=Size.COMPACTO,
            parking_type=ParkingType.ASSIGNMENT,
            is_assignment=True,
            notified_by=self.user
        )
        transfer_parking_url = reverse('transfer_parking', kwargs={'parking_id': parking.id})
        
        response = self.client.put(transfer_parking_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Parking assigned", response.json()["message"])

    def test_assign_parking_already_assigned(self):
        parking = Parking.objects.create(
            location=Point(2.1734, 42.3851, srid=4326),
            size=Size.COMPACTO,
            parking_type=ParkingType.FREE,
            is_assignment=True,
            notified_by=self.user
        )
        assign_parking_url = reverse('assign_parking', kwargs={'parking_id': parking.id})
        
        response = self.client.put(assign_parking_url)
        self.assertNotEqual(response.status_code, 200)

    def test_delete_parking_success(self):
        parking = Parking.objects.create(
            location=Point(2.1734, 42.3851, srid=4326),
            size=Size.COMPACTO,
            parking_type=ParkingType.FREE,
            is_assignment=False,
            notified_by=self.user
        )
        delete_parking_url = reverse('delete_parking', kwargs={'parking_id': parking.id})
        
        response = self.client.delete(delete_parking_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Parking deleted", response.json()["message"])

    def test_get_parking_near_success(self):
        Parking.objects.create(
            location=Point(2.1734, 42.3851, srid=4326),
            size=Size.BERLINA,
            parking_type=ParkingType.FREE,
            is_assignment=False,
            notified_by=self.user
        )
        Parking.objects.create(
            location=Point(2.1744, 42.3852, srid=4326),
            size=Size.COMPACTO,
            parking_type=ParkingType.FREE,
            is_assignment=False,
            notified_by=self.user
        )

        City.objects.create(
            name="Barcelona",
            name_ascii="Barcelona",
            alternative_name="Barna",
            location=Point(2.1734, 42.3851, srid=4326),
            country_code="ES"
        )
        
        get_parking_near_url = reverse('near')
        
        data = {
            "latitude": "42.3851",
            "longitude": "2.1734",
        }

        response = self.client.post(get_parking_near_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0, "Debería encontrar aparcamientos cercanos")


