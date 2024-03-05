from django.urls import reverse
from rest_framework.test import APITestCase
from apps.authentication.models import CustomUser
from django.test import TestCase, Client
from rest_framework import status
from apps.authentication.serializers import UserSerializer
from datetime import date
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
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')

    def test_register(self):
        url = reverse('register')
        data = {'username': 'newuser', 'email': 'newuser@admin.com', 'password': 'newpassword', 'dni': '12345679Z', 'phone': '+34600000000', 'birth_date': '1990-01-01'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')

    def test_logout(self):
        # Primero, inicia sesión
        self.client.login(email=self.email, password=self.password)
        # Luego, prueba el logout
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')




class UsersListTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        # Crear un usuario administrador para las pruebas
        self.admin = CustomUser.objects.create_superuser(username='admin', email='admin@admin.com', password='admin', dni='12345678Z', phone='+34600000000', birth_date='1990-01-01')

    def test_get_users_list(self):
        # Autenticar como usuario administrador
        self.client.force_login(self.admin)
        
        # Crear algunos usuarios de prueba
        user1 = CustomUser.objects.create(username="user1", email="user1@example.com", 
                                           dni="12345678A", birth_date=date(1990, 1, 1), 
                                           phone="+123456789")
        user2 = CustomUser.objects.create(username="user2", email="user2@example.com", 
                                           dni="23456789B", birth_date=date(1995, 1, 1), 
                                           phone="+234567890")
        
        # Realizar una solicitud GET sin parámetros de filtro
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que se devuelvan todos los usuarios
        expected_data = UserSerializer([self.admin,user1, user2], many=True).data
        self.assertEqual(response.json(), expected_data)

        # Realizar una solicitud GET con un parámetro de filtro
        response = self.client.get('/api/users', {'username': 'user1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que se devuelva solo el usuario filtrado
        expected_data = UserSerializer([user1], many=True).data
        self.assertEqual(response.json(), expected_data)

    def test_delete_users_list(self):
        # Autenticar como usuario administrador
        self.client.force_login(self.admin)
        
        # Crear algunos usuarios de prueba
        CustomUser.objects.create(username="user1", email="user1@example.com", 
                                  dni="12345678A", birth_date=date(1990, 1, 1), 
                                  phone="+123456789")
        CustomUser.objects.create(username="user2", email="user2@example.com", 
                                  dni="23456789B", birth_date=date(1995, 1, 1), 
                                  phone="+234567890")

        # Realizar una solicitud DELETE
        response = self.client.delete('/api/users')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verificar que todos los usuarios se hayan eliminado
        self.assertEqual(CustomUser.objects.count(), 0)