from django.db import models

from apps.authentication.models import CustomUser
from apps.payment.enums import MemberType,MemberId

class Credit(models.Model):
    value = models.IntegerField(blank=False, null=False)
    creation_date = models.DateField(auto_now_add=True, blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)

    def to_json(self):
        return {
            'id': self.id,
            'value': self.value
        }

class MemberShip(models.Model):
    start_date=models.DateTimeField(blank=False, null=False)
    end_date=models.DateTimeField(blank=False, null=False)
    type = models.CharField(max_length=16, choices=MemberType.choices(), default=MemberType.FREE, blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type
        }
    