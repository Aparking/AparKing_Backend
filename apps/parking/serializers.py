from apps.parking.models import Parking
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField

class ParkingSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Parking
        fields = '__all__'
        geo_field = 'location'

    def create(self, validated_data):
        
        return super().create(validated_data)

    def get_location(self, obj):
        if obj.location:
            return obj.location.y, obj.location.x
        else:
            return None