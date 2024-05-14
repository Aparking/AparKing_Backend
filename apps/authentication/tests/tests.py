from rest_framework.authtoken.models import Token
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from apps.authentication.models import CustomUser
from rest_framework.test import APIClient, APITestCase
from apps.authentication.enums import Gender
from django.urls import reverse


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


class UsersListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = CustomUser.objects.create(
            username='adminuser',
            email='adminuser@example.com',
            dni='12345678Z',
            birth_date='2000-01-01',
            gender=Gender.MALE,
            phone='123456789',
            iban='ES9121000418450051332',
            is_staff=True
        )
        self.normal_user = CustomUser.objects.create(
            username='normaluser',
            email='normaluser@example.com',
            dni='87654321Z',
            birth_date='2000-01-01',
            gender=Gender.FEMALE,
            phone='987654321',
            iban='ES9121000418450200051332',
            is_staff=False
        )
        self.client = APIClient()

    # Comprueba que el administrador puede tener acceso al listado de usuarios
    def test_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url_users = reverse('users-list')
        response = self.client.get(url_users)
        self.assertEqual(response.status_code, 200)

    # Comprueba que un administrador puede hacer un get de todos los usuarios
    def test_get_all_users(self):
        self.client.force_authenticate(user=self.admin_user)
        url_users = reverse('users-list')
        response = self.client.get(url_users)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    # Comprueba que un usuario administrador puede filtrar a los usuarios
    def test_filter_users_by_username(self):
        self.client.force_authenticate(user=self.admin_user)
        url_users = reverse('users-list')
        response = self.client.get(url_users, {'username': 'normaluser'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    # Comprueba que un administrador no puede crear un usuario con campos inválidos
    def test_create_user_with_invalid_data(self):
        self.client.force_authenticate(user=self.admin_user)
        url_users = reverse('users-list')
        response = self.client.post(url_users, {'username': ''})
        self.assertEqual(response.status_code, 400)

    # Comprueba que un administrador puede borrar a todos los usuarios
    def test_delete_all_users(self):
        self.client.force_authenticate(user=self.admin_user)
        url_users = reverse('users-list')
        response = self.client.delete(url_users)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(CustomUser.objects.count(), 0)

class UserInfoViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            dni='12345678Z',
            birth_date='2000-01-01',
            gender=Gender.OTHER,
            phone='123456789',
            iban='ES9121000418450200051332',
            is_staff=False
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_user_info_with_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url_user = reverse('userInfo')
        response = self.client.get(url_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'testuser')

    def test_user_info_with_unauthenticated_user(self):
        url_user = reverse('userInfo')
        response = self.client.get(url_user)
        self.assertEqual(response.status_code, 401)

class VerifyUserViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            dni='12345678Z',
            birth_date='2000-01-01',
            gender=Gender.MALE,
            phone='123456789',
            iban='ES9121000418450200051332',
            is_staff=False,
            code='1234'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
    def test_verify_user_with_valid_token_and_correct_code(self):
        url = reverse('verify')
        response = self.client.post(url, {'token': self.token.key, 'code': '1234'})
        self.assertEqual(response.status_code, 200)

    def test_verify_user_with_valid_token_and_incorrect_code(self):
        url = reverse('verify')
        response = self.client.post(url, {'token': self.token.key, 'code': '0000'})
        self.assertEqual(response.status_code, 400)

    def test_verify_user_with_invalid_token(self):
        url = reverse('verify')
        response = self.client.post(url, {'token': 'invalidtoken', 'code': '1234'})
        self.assertEqual(response.status_code, 400)