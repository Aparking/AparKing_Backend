from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpRequest

from apps.parking.coordenates import Coordenates
from apps.parking.models import Parking, ParkingType, ParkingSize

class ParkingFilter:
    def __init__(self, location: Point, size: ParkingSize|None, parking_type: ParkingType|None, quantity: int):
        self.location = location
        self.size = size
        self.parking_type = parking_type
        self.quantity = quantity

    @staticmethod
    def from_request(request: HttpRequest):
        location = Coordenates.from_request(request).get_point()
        if location:
            size = ParkingSize[request.POST.get('parking_size').upper()] if request.POST.get('parking_size') else None
            parking_type = ParkingType[request.POST.get('parking_type').upper()] if request.POST.get('parking_type') else None
            quantity = int(request.POST.get('quantity')) if request.POST.get('quantity') else None
            return ParkingFilter(location, size, parking_type, quantity)
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
        
