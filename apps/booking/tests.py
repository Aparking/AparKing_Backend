from django.test import TestCase
from django.utils import timezone
from apps.authentication.models import CustomUser
from apps.garagement.models import Garage, Address, Availability
from apps.garagement.enums import GarageStatus
from apps.booking.models import Comment,Claim,Book
from datetime import timedelta, datetime, time
import datetime as dt
from django.utils import timezone

class CommentModelTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            street_number='123',
            address_line='Test Street',
            city='Test City',
            region='Test Region',
            country='US',
            postal_code='12345'
        )
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com', dni='12345678A',
                                        birth_date=dt.date(1990, 1, 1), gender="M", phone='+123456789')  
        self.garage = Garage.objects.create(name='Test Garage',  description='Test description',
            height=2.5,
            width=5.0,
            length=5.0,
            price=100.00,
            owner=self.user,
            address=self.address)
        self.comment = Comment.objects.create(
            title='Great service',
            description='The service was excellent...',
            rating=5,
            user=self.user,
            garage=self.garage
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.title, 'Great service')
        self.assertEqual(self.comment.rating, 5)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.garage, self.garage)

    def test_comment_string_representation(self):
        self.assertEqual(str(self.comment), f'{self.garage.name} : {self.comment.title}')
        
  
  
class ClaimModelTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            street_number='123',
            address_line='Test Street',
            city='Test City',
            region='Test Region',
            country='US',
            postal_code='12345'
        )
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com', dni='12345678A',
                                        birth_date=dt.date(1990, 1, 1), gender="M", phone='+123456789')  
        self.garage = Garage.objects.create(name='Test Garage',  description='Test description',
            height=2.5,
            width=5.0,
            length=5.0,
            price=100.00,
            owner=self.user,
            address=self.address)
        self.claim = Claim.objects.create(
            title='Issue with service',
            description='I had a problem with...',
            user=self.user,
            garage=self.garage,
            status='PENDING'
        )

    def test_claim_creation(self):
        self.assertEqual(self.claim.title, 'Issue with service')
        self.assertEqual(self.claim.status, 'PENDING')
        self.assertTrue(self.claim.publication_date <= 
                        dt.date(9999, 1, 1))

    def test_claim_string_representation(self):
        self.assertEqual(str(self.claim), f'{self.garage.name} : {self.claim.title}')
        
class BookModelTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            street_number='123',
            address_line='Test Street',
            city='Test City',
            region='Test Region',
            country='US',
            postal_code='12345'
        )
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com', dni='12345678A',
                                        birth_date=dt.date(1990, 1, 1), gender="M", phone='+123456789')  
        self.garage = Garage.objects.create(name='Test Garage',  description='Test description',
            height=2.5,
            width=5.0,
            length=5.0,
            price=100.00,
            owner=self.user,
            address=self.address)
        self.availability = Availability.objects.create(
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=7),
            status=GarageStatus.AVAILABLE,
            garage=self.garage
        )
        self.book = Book.objects.create(
            user=self.user,
            payment_method='CASH',
            status='PENDING',
            availability= self.availability
        )

    def test_book_creation(self):
        self.assertEqual(self.book.status, 'PENDING')
        self.assertEqual(self.book.payment_method, 'CASH')

    def test_book_total_price_calculation(self):
        days_difference = (self.availability.end_date.date() - self.availability.start_date.date()).days
        total_price = self.book.calculate_total_price()
        expected_price = days_difference * self.garage.price
        self.assertEqual(total_price, expected_price)

    def test_book_string_representation(self):
        username = self.user.username if self.user else None
        self.assertEqual(str(self.book), f"{username} : {self.availability.garage.name} - {self.availability.start_date} - {self.availability.end_date}")
        
class CreateCommentTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('testuser', 'test@example.com', 'password123')
        self.other_user = CustomUser.objects.create_user('otheruser', 'other@example.com', 'password123')
        
        self.address = Address.objects.create(
            street_number='123',
            address_line='Main Street',
            city='City',
            region='Region',
            country='US',
            postal_code='12345'
        )
        
        self.garage = Garage.objects.create(
            name='Test Garage',
            description='Test Description',
            height=2.5,
            width=2.5,
            length=5.0,
            price=100,
            owner=self.user,
            address=self.address
        )
        
        self.availability = Availability.objects.create(
            start_date=dt.datetime.now(),
            end_date=dt.datetime.now() + timedelta(days=1),
            status=GarageStatus.AVAILABLE.name,
            garage=self.garage
        )
        
        self.book = Book.objects.create(
            payment_method='CASH',
            status='CONFIRMED',
            user=self.user,
            availability=self.availability
        )
    
    def test_user_can_create_comment(self):
        self.client.login(username='testuser', password='password123')
        
        response = self.client.post('/path/to/create/comment/', {
            'title': 'Great Garage',
            'description': 'This garage was very convenient.',
            'rating': 5,
            'garage': self.garage.pk,
            'user': self.user.pk
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.title, 'Great Garage')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.garage, self.garage)

    def test_non_user_cannot_create_comment(self):
        response = self.client.post('/path/to/create/comment/', {
            'title': 'Unauthorized Comment',
            'description': 'This should not work.',
            'rating': 1,
            'garage': self.garage.pk,
            'user': self.other_user.pk
        })
        
        self.assertNotEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 0)

