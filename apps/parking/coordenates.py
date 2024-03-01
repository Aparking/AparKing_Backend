from django.contrib.gis.geos import Point
from django.http import HttpRequest

class Coordenates:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
    
    @staticmethod
    def from_request(request: HttpRequest):
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if longitude and latitude:
            return Coordenates(float(latitude), float(longitude))
        return None
      
    def get_point(self):
        return Point(self.latitude, self.longitude, srid=4326)