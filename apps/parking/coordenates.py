from django.contrib.gis.geos import Point
from django.http import HttpRequest

class Coordenates:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
    
    @staticmethod
    def from_request(request: HttpRequest):
        latitude = request.POST.get('latitude') if request.POST.get('latitude') else request.data.get('latitude')
        longitude = request.POST.get('longitude') if request.POST.get('longitude') else request.data.get('longitude')
        if longitude and latitude:
            return Coordenates(float(latitude), float(longitude))
        return None
      
    def get_point(self):
        return Point(self.latitude, self.longitude, srid=4326)