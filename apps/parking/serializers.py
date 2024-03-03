from django.contrib.gis.geos import Point
from rest_framework import serializers
from apps.parking.models import Parking
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from apps.parking.enums import ParkingType

class ParkingSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Parking
        fields = '__all__'
        extra_kwargs = {
            'location': {'required': False},
            'notified_by': {'read_only': True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.location:
            representation['location'] = {
                'latitude': instance.location.y,
                'longitude': instance.location.x
            }
        return representation
    
    def validate(self, attrs):
        latitude = attrs.get('latitude')
        longitude = attrs.get('longitude')

        if latitude is not None and longitude is not None:
            location = Point(longitude, latitude, srid=4326)
            exist = Parking.objects.annotate(distance=Distance('location', location)).filter(
                location__distance_lte=(location, D(m=10)),
                parking_type=ParkingType.FREE,
                is_transfer=False
            ).exists()

            if exist:
                raise serializers.ValidationError({'location': 'There is already a parking near you'})

        return super().validate(attrs)

    def create(self, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)

        if latitude is not None and longitude is not None:
            validated_data['location'] = Point(longitude, latitude, srid=4326)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)

        if latitude is not None and longitude is not None:
            instance.location = Point(longitude, latitude, srid=4326)

        instance.save()
        return super().update(instance, validated_data)