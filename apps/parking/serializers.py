from rest_framework import serializers
from apps.parking.models import Parking
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField


class ParkingSerializer(GeoFeatureModelSerializer):
    location = GeometrySerializerMethodField()

    def validate(self, data):
        if data['location'] == None or data['size'] == None or data['parking_type'] == None or data['notified_by'] == None:
            raise serializers.ValidationError("Datos erróneos")
        return data
    class Meta:
        model = Parking
        fields = '__all__'
        geo_field = 'location'

    def get_location(self, obj):
        if obj.location:
            return obj.location.y, obj.location.x
        else:
            return None