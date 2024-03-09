from rest_framework import serializers
from .models import Credit, MemberShip

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ['id', 'value', 'creation_date', 'user']

class MemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        fields = ['id', 'start_date', 'end_date', 'type', 'user','price']

