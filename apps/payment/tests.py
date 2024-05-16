import datetime
from django.test import TestCase
from django.utils import timezone
from apps.authentication.models import CustomUser
from apps.payment.enums import MemberType

from apps.payment.models import Credit, MemberShip

import json
import stripe
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from apps.authentication.models import CustomUser
from apps.payment.enums import MemberType, MemberId
from apps.payment.models import Credit, MemberShip

class CreditTestCase(TestCase):
    def setUp(self):
     self.user = CustomUser.objects.create(username='testuser', email='test@example.com', dni='12345678A',
                                           birth_date=datetime.date(1990, 1, 1), gender="M", phone='+123456789')        
     self.credit = Credit.objects.create(value=100, user=self.user)
     
    def test_credit_value(self):
        self.assertEqual(self.credit.value, 100)

    def test_credit_creation_date(self):
        self.assertIsNotNone(self.credit.creation_date)

    def test_credit_user(self):
        self.assertEqual(self.credit.user, self.user)
        
    def test_credit_creation_and_retrieval(self):
        credits = Credit.objects.filter(user=self.user)
        self.assertEqual(credits.count(), 1)
        self.assertEqual(credits[0].value, 100)
        
class MemberShipTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com', dni='12345678A',
                                            birth_date=datetime.date(1990, 1, 1), gender="M", phone='+123456789')
        self.membership = MemberShip.objects.create(start_date=timezone.now(),
                                                    end_date=timezone.now() + datetime.timedelta(days=30),
                                                    type=MemberType.KING,
                                                    user=self.user                                                  
                                                    )

    def test_membership_start_date(self):
        self.assertIsNotNone(self.membership.start_date)

    def test_membership_end_date(self):
        self.assertIsNotNone(self.membership.end_date)

    def test_membership_type(self):
        self.assertEqual(self.membership.type, MemberType.KING)

    def test_membership_user(self):
        self.assertEqual(self.membership.user, self.user)
        
    def test_membership_creation_and_retrieval(self):
        memberships = MemberShip.objects.filter(user=self.user)
        self.assertEqual(memberships.count(), 1)
        self.assertEqual(memberships[0].type, 'King')

class CreateCheckoutSessionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', dni='12345678A',
                                                   birth_date=datetime.date(1990, 1, 1), gender="M", phone='+123456789', password='testpassword')
        self.credit = Credit.objects.create(value=100, user=self.user)
        self.membership = MemberShip.objects.create(start_date=timezone.now(),
                                                    end_date=timezone.now() + datetime.timedelta(days=30),
                                                    type=MemberType.KING,
                                                    user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('create_checkout_session')

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_noble_plan(self, mock_stripe_create):
        mock_checkout_session = MagicMock()
        mock_checkout_session.id = 'cs_test_id'
        mock_checkout_session.url = 'https://example.com/success'
        mock_stripe_create.return_value = mock_checkout_session

        data = {
            'planId': 'NOBLE',
            'url': 'https://example.com/success'
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertIn('url', response_data)
        self.assertIn('user_info', response_data)
        self.assertEqual(response_data['user_info']['credit'], 300)

        self.user.refresh_from_db()
        self.assertEqual(self.user.stripe_session_id, 'cs_test_id')

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_king_plan(self, mock_stripe_create):
        mock_checkout_session = MagicMock()
        mock_checkout_session.id = 'cs_test_id'
        mock_checkout_session.url = 'https://example.com/success'
        mock_stripe_create.return_value = mock_checkout_session

        data = {
            'planId': 'KING',
            'url': 'https://example.com/success'
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertIn('url', response_data)
        self.assertIn('user_info', response_data)
        self.assertEqual(response_data['user_info']['credit'], 1000)

        self.user.refresh_from_db()
        self.assertEqual(self.user.stripe_session_id, 'cs_test_id')

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_stripe_error(self, mock_stripe_create):
        mock_stripe_create.side_effect = stripe.error.StripeError("Stripe error occurred")

        data = {
            'planId': 'KING',
            'url': 'https://example.com/failure'
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Stripe error occurred')

class GetMembershipTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', dni='12345678A',
                                                   birth_date=datetime.date(1990, 1, 1), gender="M", phone='+123456789', password='testpassword')
        self.credit = Credit.objects.create(value=100, user=self.user)
        self.membership = MemberShip.objects.create(start_date=timezone.now(),
                                                    end_date=timezone.now() + datetime.timedelta(days=30),
                                                    type=MemberType.KING,
                                                    user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('getMembership')

    @patch('stripe.checkout.Session.retrieve')
    def test_get_membership_with_valid_stripe_session_noble(self, mock_stripe_retrieve):
        mock_session = MagicMock()
        mock_session.line_items.data = [
            MagicMock(price=MagicMock(id=str(MemberId.NOBLE)), quantity=1)
        ]
        mock_session.payment_status = "paid"
        mock_session.status = "complete"
        mock_stripe_retrieve.return_value = mock_session
        self.user.stripe_session_id = 'cs_test_id'
        self.user.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertIn('user_info', response_data)
        user_info = response_data['user_info']
        self.assertEqual(user_info['credit']['value'], 300)
        self.assertEqual(user_info['membership']['type'], MemberType.NOBLE.value)

    @patch('stripe.checkout.Session.retrieve')
    def test_get_membership_with_valid_stripe_session_king(self, mock_stripe_retrieve):
        mock_session = MagicMock()
        mock_session.line_items.data = [
            MagicMock(price=MagicMock(id=str(MemberId.KING)), quantity=1)
        ]
        mock_session.payment_status = "paid"
        mock_session.status = "complete"
        mock_stripe_retrieve.return_value = mock_session
        self.user.stripe_session_id = 'cs_test_id'
        self.user.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertIn('user_info', response_data)
        user_info = response_data['user_info']
        self.assertEqual(user_info['credit']['value'], 1000)
        self.assertEqual(user_info['membership']['type'], MemberType.KING.value)

    @patch('stripe.checkout.Session.retrieve')
    def test_get_membership_with_valid_stripe_session_other(self, mock_stripe_retrieve):
        mock_session = MagicMock()
        mock_session.line_items.data = [
            MagicMock(price=MagicMock(id="other_plan_id"), quantity=1)
        ]
        mock_session.payment_status = "paid"
        mock_session.status = "complete"
        mock_stripe_retrieve.return_value = mock_session
        self.user.stripe_session_id = 'cs_test_id'
        self.user.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertIn('user_info', response_data)
        user_info = response_data['user_info']
        self.assertEqual(user_info['credit']['value'], 50)  
        self.assertEqual(user_info['membership']['type'], MemberType.FREE.value)  

    @patch('stripe.checkout.Session.retrieve')
    def test_get_membership_with_no_stripe_session(self, mock_stripe_retrieve):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertIn('user_info', response_data)
        user_info = response_data['user_info']
        self.assertEqual(user_info['credit']['value'], 100)
        self.assertEqual(user_info['membership']['type'], MemberType.KING.value)

    @patch('stripe.checkout.Session.retrieve')
    def test_get_membership_with_stripe_error(self, mock_stripe_retrieve):
        mock_stripe_retrieve.side_effect = stripe.error.StripeError("Stripe error occurred")
        self.user.stripe_session_id = 'cs_test_id'
        self.user.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Stripe error occurred')

    @patch('stripe.checkout.Session.retrieve')
    def test_get_membership_with_valid_stripe_credit_session(self, mock_stripe_retrieve):
        mock_session = MagicMock()
        mock_session.line_items.data = [
            MagicMock(price=MagicMock(id="credit_plan_id"), quantity=10)
        ]
        mock_session.payment_status = "paid"
        mock_session.status = "complete"
        mock_stripe_retrieve.return_value = mock_session
        self.user.stripe_credit_id = 'cs_credit_test_id'
        self.user.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertIn('user_info', response_data)
        user_info = response_data['user_info']
        self.assertEqual(user_info['credit']['value'], 110)

        self.user.refresh_from_db()  # Refresh the user from the database to get the updated values
        self.assertIsNone(self.user.stripe_credit_id)

class CreateCheckoutSessionCreditTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', dni='12345678A',
                                                   birth_date=datetime.date(1990, 1, 1), gender="M", phone='+123456789', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('create_checkout_session_credit')

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_credit_success(self, mock_stripe_create):
        mock_checkout_session = MagicMock()
        mock_checkout_session.id = 'cs_test_id'
        mock_checkout_session.url = 'https://example.com/success'
        mock_stripe_create.return_value = mock_checkout_session

        data = {
            'credit': 10,
            'url': 'https://example.com/success'
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('url', response_data)
        self.assertIn('user_info', response_data)
        self.assertEqual(response_data['user_info']['username'], self.user.username)
        self.assertEqual(response_data['user_info']['email'], self.user.email)
        self.assertEqual(response_data['user_info']['id'], self.user.id)

        self.user.refresh_from_db()
        self.assertEqual(self.user.stripe_credit_id, 'cs_test_id')

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_credit_stripe_error(self, mock_stripe_create):
        mock_stripe_create.side_effect = stripe.error.StripeError("Stripe error occurred")

        data = {
            'credit': 10,
            'url': 'https://example.com/failure'
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Stripe error occurred')