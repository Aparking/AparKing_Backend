import datetime
from django.test import TestCase
from django.utils import timezone
from apps.authentication.models import CustomUser
from apps.payment.enums import MemberType

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
        # self.user = CustomUser.objects.create(username='testuser', email='test@example.com', dni='12345678A',
        #                                    birth_date=datetime.date(1990, 1, 1), gender="M", phone='+123456789')
        self.membership = MemberShip.objects.create(start_date=timezone.now(),
                                                    end_date=timezone.now() + datetime.timedelta(days=30),
                                                    type=MemberType.KING
                                                  )

    def test_membership_start_date(self):
        self.assertIsNotNone(self.membership.start_date)

    def test_membership_end_date(self):
        self.assertIsNotNone(self.membership.end_date)

    def test_membership_type(self):
        self.assertEqual(self.membership.type, MemberType.KING)

    # def test_membership_user(self):
    #     self.assertEqual(self.membership.user, self.user)
