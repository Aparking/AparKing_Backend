from django.db import models
from datetime import datetime
from apps.authentication.models import CustomUser
from apps.payment.enums import MemberType
from dateutil.relativedelta import relativedelta

class Credit(models.Model):
    value = models.IntegerField(blank=False, null=False)
    creation_date = models.DateField(auto_now_add=True, blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
class MemberShip(models.Model):
    start_date = models.DateTimeField(default=datetime.now, blank=False, null=False)
    end_date = models.DateTimeField(default=datetime.now()+relativedelta(months=+1), blank=False, null=False)
    type = models.CharField(max_length=16, choices=MemberType.choices(), default=MemberType.FREE, blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    price= models.DecimalField(max_digits=6, decimal_places=2,default=0.00,blank=True, null=True)