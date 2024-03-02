from apps.garagement.models import Address, Availability, Garage, Image
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
       model = Address
       fields = '__all__'
       
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
       model = Image
       fields ='__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
       model = Availability
       fields = '__all__'

class GarageSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Garage
        fields = '__all__'
