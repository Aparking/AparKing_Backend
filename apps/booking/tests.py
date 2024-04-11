from datetime import date, timedelta
from django.test import TestCase
from apps.authentication.models import CustomUser
from apps.booking.enums import BookingStatus
from apps.booking.models import Book, Comment
from apps.garagement.enums import GarageStatus
from apps.garagement.models import Address, Availability, Garage
from datetime import datetime, timedelta
from rest_framework import status


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
        self.user = CustomUser.objects.create('testuser', 'test@example.com', 'password123')
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
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=5),
            status=GarageStatus.AVAILABLE.value,
            garage=self.garage
        )
        self.book = Book.objects.create(
            user=self.user,
            payment_method='CASH',
            status=BookingStatus.CONFIRMED.value,
            availability=self.availability
        )
        self.comment = Comment.objects.create(
            title='My first comment',
            description='Great experience',
            publication_date=datetime.now(),
            rating=4,
            user=self.user,
            garage=self.garage
        )

    def test_comment_creation(self):
        # Comentario creado para una reserva realizada con todos los campos válidos
        response = self.client.post('http://localhost:3000/comments/create', {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}, format='json')
        self.assertEqual(response.status_code, 201)
        comment = Comment.objects.last()
        self.assertEqual(comment.title, 'My first comment')
        self.assertEqual(comment.description, 'Great experience')
        self.assertEqual(comment.rating, 4)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.garage, self.garage)
        
    def test_comment_creation_missing_garage_id(self):
        # Comentario sin proporcionar un garage_id
        response = self.client.post('http://localhost:3000/comments/create', {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_missing_user(self):
        # Comentario sin proporcionar un user
        response = self.client.post('http://localhost:3000/comments/create', {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)      

    def test_comment_creation_with_missing_title(self):
        # Comentario sin proporcionar un title
        data = {'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_missing_description(self):
        # Comentario sin proporcionar un description
        data = {'title': 'My first comment', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    def test_comment_creation_with_missing_rating(self):
        # Comentario sin proporcionar un publication_date
        data = {'title': 'My first comment', 'description': 'Great experience', 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0) 

    def test_comment_creation_with_missing_rating(self):
        # Comentario sin proporcionar un rating
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    # Pruebas para el atributo title
    def test_comment_creation_with_empty_title(self):
        # Prueba de creación de comentario con title vacío
        data = {'title': '', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_min_title(self):
        # Prueba de creación de comentario con title mínimo válido (1 carácter)
        data = {'title': 'a', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)  
    
    def test_comment_creation_with_max_title(self):
        # Prueba de creación de comentario con title máximo válido (64 caracteres)
        data = {'title': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)  
        
    def test_comment_creation_with_max_plus_one_title(self):
        # Prueba de creación de comentario con title máximo válido menos uno (65 caracteres)
        data = {'title': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_other_chars_title(self):
        # Prueba de creación de comentario con title en otro idioma
        data = {'title': 'привет', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)  
               
    # Pruebas para el atributo description
    def test_comment_creation_with_empty_description(self):
        # Prueba de creación de comentario con description vacío
        data = {'title': 'My first comment', 'description': '', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_min_description(self):
        # Prueba de creación de comentario con description mínimo válido (1 carácter)
        data = {'title': 'My first comment', 'description': 'a', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)  
    
    def test_comment_creation_with_max_description(self):
        # Prueba de creación de comentario con description máximo válido (1024 caracteres)
        data = {'title': 'My first comment', 'description': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)  
        
    def test_comment_creation_with_max_plus_one_description(self):
        # Prueba de creación de comentario con description máximo válido menos uno (1025 caracteres)
        data = {'title': 'My first comment', 'description': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_other_chars_description(self):
        # Prueba de creación de comentario con description en otro idioma
        data = {'title': 'My first comment', 'description': 'привет', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1) 

    # Pruebas para el atributo publication_date
    def test_comment_creation_with_bad_input_on_date(self):
        # Prueba de creación de publication_date con input distinto a fecha
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':'a', 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_blank_date(self):
        # Prueba de creación de publication_date en blanco
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':'', 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
    
    def test_comment_creation_with_min_date(self):
        # Prueba de creación de publication_date mínima
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':date(2000, 1, 1), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)  

    def test_comment_creation_with_min_minus_one_date(self):
        # Prueba de creación de publication_date mínima menos uno
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':date(1999, 12, 31), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    def test_comment_creation_with_max_date(self):
        # Prueba de creación de publication_date máxima
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':date(2199, 12, 31), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)  
    
    def test_comment_creation_with_max_plus_one_date(self):
        # Prueba de creación de publication_date máxima más uno
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':date(2200, 1, 1), 'rating':4, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    # Pruebas para el atributo rating
    def test_comment_creation_with_zero_rating(self):
        # Prueba de creación de comentario con rating 0
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':0, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    def test_comment_creation_with_six_rating(self):
        # Prueba de creación de comentario con rating 6
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':6, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0) 
        
    def test_comment_creation_with_negative_rating(self):
        # Prueba de creación de comentario con rating negativo
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':-1, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  

    def test_comment_creation_with_float_rating(self):
        # Prueba de creación de comentario con rating decimal
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':3.3, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0) 
        
    def test_comment_creation_with_float_rating(self):
        # Prueba de creación de comentario con rating decimal negativo
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':-3.3, 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0) 
        
    def test_comment_creation_with_bad_input_rating(self):
        # Prueba de creación de comentario con rating distinto a un número
        data = {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':'hola', 'user':self.user, 'garage':self.garage.id}
        response = self.client.post('http://localhost:3000/comments/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)  
        
    

    def test_comment_creation_unauthenticated(self):
        # Un usuario no puede comentar un garaje si no está autenticado
        self.client.force_authenticate(user=None)
        response = self.client.post('http://localhost:3000/comments/create', {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_creation_no_bookings(self):
        # Un usuario no puede comentar un garaje si no ha hecho una reserva antes
        response = self.client.post('http://localhost:3000/comments/create', {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)
          
    def test_comment_associated_with_book(self):
        # Verifica si el comentario está asociado a una reserva
        self.assertEqual(self.comment.book, self.book)

    def test_comment_associated_with_user(self):
        # Verifica si el comentario está asociado con el usuario correcto
        self.assertEqual(self.comment.user, self.user)

    def test_comment_associated_with_garage(self):
        # Verifica si el comentario está asociado con el garaje correcto
        self.assertEqual(self.comment.garage, self.garage)
          
    def test_create_comment_with_pending_reservation(self):
        # Intenta crear un comentario para un garaje con reserva PENDING
        self.book.status = BookingStatus.PENDING.value
        self.book.save()
        response = self.client.post('http://localhost:3000/comments/create', {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_with_cancelled_reservation(self):
        # Intenta crear un comentario para un garaje con reserva CANCELLED
        self.book.status = BookingStatus.CANCELLED.value
        self.book.save()
        response = self.client.post('http://localhost:3000/comments/create', {'title': 'My first comment', 'description': 'Great experience', 'publication_date':datetime.now(), 'rating':4, 'user':self.user, 'garage':self.garage.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)