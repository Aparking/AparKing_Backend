from django.urls import reverse
from rest_framework.test import APITestCase
from apps.authentication.models import CustomUser

class AuthTestCase(APITestCase):

    email = 'admin@admin.com'
    password = 'admin'

    def setUp(self):
        super().setUp()
        self.user = CustomUser.objects.create_user(username='admin', email=self.email, password=self.password, dni='12345678Z', phone='+34600000000', birth_date='1990-01-01')

    def tearDown(self):
        super().tearDown()

    def test_login(self):
        url = reverse('login')
        data = {'password': self.password, 'email': self.email}
        response = self.client.post(url, data, format='json')
        # Asegúrate de verificar la respuesta correcta según tu implementación
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')

    def test_register(self):
        url = reverse('register')
        data = {'username': 'newuser', 'email': 'newuser@admin.com', 'password': 'newpassword', 'dni': '12345679Z', 'phone': '+34600000000', 'birth_date': '1990-01-01'}
        response = self.client.post(url, data, format='json')
        # Asegúrate de verificar la respuesta correcta según tu implementación
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')

    def test_logout(self):
        # Primero, inicia sesión
        self.client.login(email=self.email, password=self.password)
        # Luego, prueba el logout
        url = reverse('logout')
        response = self.client.get(url)  # Asegúrate de que tu endpoint de logout acepte una petición GET
        # Asegúrate de verificar la respuesta correcta según tu implementación
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')
