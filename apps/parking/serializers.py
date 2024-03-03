from rest_framework import serializers
from apps.parking.models import Parking
from apps.parking.enums import ParkingType, ParkingSize

class ParkingSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = Parking
        fields = '__all__'

    def create(self, validated_data):
        
        return super().create(validated_data)

    def get_location(self, obj):
        if obj.location:
            return {'latitude': obj.location.x, 'longitude': obj.location.y}
        else:
            return None