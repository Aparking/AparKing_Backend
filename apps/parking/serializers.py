from rest_framework import serializers
from apps.parking.models import Parking

class ParkingSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    class Meta:
        model = Parking
        fields = '__all__'

    def get_location(self, obj):
        if obj.location:
            return obj.location.y, obj.location.x
        else:
            return None