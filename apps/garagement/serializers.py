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
       
    def create(self, validated_data):
        return super().create(validated_data)

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
       model = Availability
       fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("end_date must be later than start_date")
        return data
    
class GarageSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Garage
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        garage = Garage.objects.create(address=address, **validated_data)
        return garage
    
    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("end_date must be later than start_date")
        return data