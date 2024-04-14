from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from apps.authentication.enums import Gender
from apps.authentication.models import CustomUser
from apps.booking.enums import BookingStatus
from apps.booking.models import Book, Comment
from apps.garagement.enums import GarageStatus
from apps.garagement.models import Address, Availability, Garage
from datetime import datetime, timedelta
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token


User = get_user_model()


class CommentCreationTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            street_number='123',
            address_line='Main Street',
            city='City',
            region='Region',
            country='US',
            postal_code='12345'
        ) 
        
        self.user = CustomUser.objects.create(
            username='testuser', 
            email='test@example.com', 
            dni='12345678Z',
            birth_date=date(1990, 1, 1),
            gender=Gender.MALE.value,
            photo="https://www.google.com",
            phone='+34600100200',
            code='123456', 
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user) 
        
        self.garage = Garage.objects.create(
            name='Sample Garage',
            description='A sample garage for testing',
            height=2.0,
            width=2.0,
            length=4.0,
            price=50.00,
            owner=self.user,
            address=self.address
        )
        
        self.availability = Availability.objects.create(
            start_date=timezone.make_aware(datetime(2024, 3, 20)),
            end_date=timezone.make_aware(datetime(2024, 3, 25)),
            status=GarageStatus.AVAILABLE.value,
            garage=self.garage
        )
        
        self.book = Book.objects.create(
            user=self.user,
            payment_method='CASH',
            status=BookingStatus.CONFIRMED.value,
            availability=self.availability
        )

    def test_comment_creation(self):
        # Comentario creado para una reserva realizada con todos los campos válidos
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)  # Obtener el token de autenticación para testuser
        data = {
            'title': 'My first comment',
            'description': 'Great experience',
            'publication_date': datetime.now(),
            'rating': 4, 
            'user': 1,
            'garage': self.garage.id
        } 
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.last()
        self.assertEqual(comment.title, 'My first comment')
        self.assertEqual(comment.description, 'Great experience')
        self.assertEqual(comment.rating, 4)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.garage, self.garage)
        self.assertEqual(Comment.objects.count(), 1)
        
    def test_comment_creation_missing_garage(self):
        # Comentario sin proporcionar un garage_id
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        data = {
            'title': 'My first comment',
            'description': 'Great experience',
            'publication_date': datetime.now(),
            'rating': 4, 
            'user': 1,
        } 
        auth_header = 'Token {}'.format(self.token.key)
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_missing_user(self):
        # Comentario sin proporcionar un user
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        data = {
            'title': 'My first comment',
            'description': 'Great experience',
            'publication_date': datetime.now(),
            'rating': 4, 
            'garage': self.garage.id
        } 
        auth_header = 'Token {}'.format(self.token.key)
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)      

    def test_comment_creation_with_missing_title(self):
        # Comentario sin proporcionar un title
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'description': 'Great experience', 
            'publication_date': datetime.now(), 
            'rating':4, 
            'user':1, 
            'garage':self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_missing_description(self):
        # Comentario sin proporcionar un description
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'publication_date':datetime.now(), 
            'rating':4, 
            'user':1, 
            'garage':self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    def test_comment_creation_with_missing_rating(self):
        # Comentario sin proporcionar un publication_date
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'rating':4, 
            'user':1, 
            'garage':self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0) 

    def test_comment_creation_with_missing_rating(self):
        # Comentario sin proporcionar un rating
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'user':1, 
            'garage':self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    # Pruebas para el atributo title
    def test_comment_creation_with_empty_title(self):
        # Prueba de creación de comentario con title vacío
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': '',
            'description': 'Great experience',
            'publication_date': datetime.now(),
            'rating': 4, 
            'user': 1,
            'garage': self.garage.id
        } 
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_max_plus_one_title(self):
        # Prueba de creación de comentario con title máximo válido menos uno (65 caracteres)
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'a' * 65,
            'description': 'Great experience',
            'publication_date': datetime.now(),
            'rating': 4, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
               
    # Pruebas para el atributo description
    def test_comment_creation_with_empty_description(self):
        # Prueba de creación de comentario con description vacío
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': '', 
            'publication_date': datetime.now(),
            'rating': 4, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_max_plus_one_description(self):
        # Prueba de creación de comentario con description máximo válido menos uno (1025 caracteres)
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 
            'publication_date': datetime.now(),
            'rating': 4, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    # Pruebas para el atributo publication_date
    def test_comment_creation_with_bad_input_on_date(self):
        # Prueba de creación de publication_date con input distinto a fecha
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':'a', 
            'rating':4, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_blank_date(self):
        # Prueba de creación de publication_date en blanco
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':'', 
            'rating':4, 
            'user': 1,
            'garage': self.garage.id
            }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
    
    def test_comment_creation_with_min_minus_one_date(self):
        # Prueba de creación de publication_date mínima menos uno
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':date(1999, 12, 31), 
            'rating':4, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)   
  
    def test_comment_creation_with_max_plus_one_date(self):
        # Prueba de creación de publication_date máxima más uno
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':date(2200, 1, 1), 
            'rating':4, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    # Pruebas para el atributo rating
    def test_comment_creation_with_zero_rating(self):
        # Prueba de creación de comentario con rating 0
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'rating':0, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    def test_comment_creation_with_six_rating(self):
        # Prueba de creación de comentario con rating 6
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'rating':6, 
            'user': 1,
            'garage': self.garage.id
            }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0) 
        
    def test_comment_creation_with_negative_rating(self):
        # Prueba de creación de comentario con rating negativo
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'rating':-1, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    def test_comment_creation_with_float_rating(self):
        # Prueba de creación de comentario con rating decimal
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'rating':3.3, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0) 
        
    def test_comment_creation_with_float_rating(self):
        # Prueba de creación de comentario con rating decimal negativo
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'rating':-3.3, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0) 
        
    def test_comment_creation_with_bad_input_rating(self):
        # Prueba de creación de comentario con rating distinto a un número
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'rating':'hola', 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    
    def test_comment_creation_unauthenticated(self):
        # Un usuario no puede comentar un garaje si no está autenticado
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'rating':4, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_creation_no_bookings(self):
        # Un usuario no puede comentar un garaje si no ha hecho una reserva antes
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'rating':4, 
            'user': 1,
            'garage': self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)
          
    def test_create_comment_with_pending_reservation(self):
        # Intenta crear un comentario para un garaje con reserva PENDING
        self.book.status = BookingStatus.PENDING.value
        self.book.save()
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        auth_header = 'Token {}'.format(self.token.key)
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'rating':4, 
            'user':1, 
            'garage':self.garage.id
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_with_cancelled_reservation(self):
        # Intenta crear un comentario para un garaje con reserva CANCELLED
        self.book.status = BookingStatus.CANCELLED.value
        self.book.save()
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_comment')
        data = {
            'title': 'My first comment', 
            'description': 'Great experience', 
            'publication_date':datetime.now(), 
            'rating':4, 
            'user':1, 
            'garage':self.garage.id
        }
        auth_header = 'Token {}'.format(self.token.key)
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
