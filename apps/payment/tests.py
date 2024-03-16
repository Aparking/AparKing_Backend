import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from apps.authentication.models import CustomUser
from apps.authentication.serializers import UserSerializer
from apps.payment.enums import MemberType
from rest_framework import status
import json
from apps.payment.models import Credit, MemberShip

class CreditTestCase(TestCase):
    def setUp(self):
     self.user = CustomUser.objects.create(username='testuser', email='test@example.com', dni='12345678A',
                                           birth_date=datetime.date(1990, 1, 1), gender="M", phone='+12345678916')        
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
                                            birth_date=datetime.date(1990, 1, 1), gender="M", phone='+12345678916')
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


class PricingPlanTestCase(TestCase):
    email = 'admin@admin.com'
    password = 'admin'

    def setUp(self):
        super().setUp()

        self.user = CustomUser.objects.create_user(username='admin', email=self.email, password=self.password, dni='12345678Z', phone='+34600000000', birth_date='1990-01-01')
        url = reverse('login')
        data = {'password': self.password, 'email': self.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')

    def test_pricingPlan(self):
        # Datos para la solicitud de pricingPlan
        user = CustomUser.objects.create_user(username='test', email='test@gmail.com', password='pbkdf2_sha256$720000$inITLGUIGyLddqe2uVcLzu$WRymtYgVsN8bq5q14fxJthCk1Kf3txgPubSjp8Q9n9U=', dni='31016814K', phone='+34664030994', birth_date='2024-03-01', is_staff=False)
        user_serializer = UserSerializer(user)
        user_data = user_serializer.data
        data = {
            'user': user_data,
            'type': 'Noble',
            'price': '3.99'
        }
        data_json = json.dumps(data)

        # Realizamos una solicitud POST a la vista 'pricingPlan'
        response = self.client.post('/pricing-plan/', data_json, content_type='application/json')
        # Verificamos que la solicitud haya sido exitosa (código de estado 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificamos que se haya creado una membresía para el usuario
        membership = MemberShip.objects.filter(user_id=user.id).first()
        self.assertIsNotNone(membership)
        self.assertEqual(membership.type, 'Noble')
        # Verificamos que se hayan asignado los créditos correspondientes al usuario
        credits = Credit.objects.filter(user_id=user.id).first()
        self.assertIsNotNone(credits)
        self.assertEqual(credits.value, 100)  # Según el tipo de plan 'Noble'

    def test_pricingPlan_invalid_user(self):
        # Datos para la solicitud de pricingPlan con un usuario inválido
        user_data = {}
        data = {
            'type': 'Noble',
            'price': '3.99'
        }
        data_json = json.dumps(data)

        # Realizamos una solicitud POST a la vista 'pricingPlan'
        response = self.client.post('/pricing-plan/', data_json, content_type='application/json')
        # Verificamos que la solicitud haya fallado (código de estado 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pricingPlan_invalid_type(self):
        # Datos para la solicitud de pricingPlan con un tipo de plan inválido
        user = CustomUser.objects.create_user(username='test', email='test@gmail.com', password='pbkdf2_sha256$720000$inITLGUIGyLddqe2uVcLzu$WRymtYgVsN8bq5q14fxJthCk1Kf3txgPubSjp8Q9n9U=', dni='31016814K', phone='+34664030994', birth_date='2024-03-01', is_staff=False)
        user_serializer = UserSerializer(user)
        user_data = user_serializer.data
        data = {
            'user': user_data,
            'type': 1111111111111,  # Este tipo de plan no existe
            'price': '3.99'
        }
        data_json = json.dumps(data)

        # Realizamos una solicitud POST a la vista 'pricingPlan'
        response = self.client.post('/pricing-plan/', data_json, content_type='application/json')
        # Verificamos que la solicitud haya fallado (código de estado 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)