from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from apps.authentication.models import CustomUser

class AuthTestCase(APITestCase):

    email = 'admin@admin.com'
    password = 'admin'

    def setUp(self):
        super().setUp()
        self.user = CustomUser.objects.create_user(
            username='admin', 
            email=self.email, 
            password=self.password, 
            dni='12345678Z', 
            phone='+34600000000', 
            birth_date='1990-01-01')

    def tearDown(self):
        super().tearDown()

    def test_login(self):
        url = reverse('login')
        data = {'password': self.password, 'email': self.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        url = reverse('register')
        data = {'username': 'newuser', 'email': 'newuser@admin.com', 'password': 'newpassword', 'dni': '12345679Z', 'phone': '+34600000000', 'birth_date': '1990-01-01'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        url_login = reverse('login')
        # Primero, inicia sesión
        data = {'password': self.password, 'email': self.email}
        response = self.client.post(url_login, data, format='json')
        # Luego, prueba el logout
        token = response.data.get('token')
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
