from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpRequest

from apps.parking.coordenates import Coordenates
from apps.parking.models import Parking, ParkingType, Size

class ParkingFilter:
    def __init__(self, location: Point, size: Size|None, parking_type: ParkingType|None, quantity: int):
        self.location = location
        self.size = size
        self.parking_type = parking_type
        self.quantity = quantity

    @staticmethod
    def from_request(request: HttpRequest):
        location = Coordenates.from_request(request)
        if location:
            location_point = location.get_point()
            size = Size[request.data.get('parking_size').upper()] if request.data.get('parking_size') else None
            parking_type = ParkingType[request.data.get('parking_type').upper()] if request.data.get('parking_type') else None
            quantity = int(request.data.get('quantity')) if request.data.get('quantity') else None
            return ParkingFilter(location_point, size, parking_type, quantity)
        return None
    
    def get_queryset(self):
        queryset = Parking.objects.all()
        if self.location:
            queryset = queryset.annotate(distance=Distance('location', self.location)).order_by('distance')
        if self.size:
            queryset = queryset.filter(size=self.size)
        if self.parking_type:
            queryset = queryset.filter(parking_type=self.parking_type)
        if self.quantity:
            queryset = queryset[:self.quantity]
        return queryset
        
