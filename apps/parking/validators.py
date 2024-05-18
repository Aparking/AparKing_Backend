from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.db.models import Q

from apps.parking.forms import ParkingForm
from apps.parking.models import Parking, ParkingType

class ParkingValidator:
    def __init__(self, form: Parking):
        self.form = form
        self.errors = {}
    
    def validate_distance(self):
        exist = Parking.objects.annotate(distance=Distance('location', self.form.location)).filter(
                    Q(location__distance_lte=(self.form.location, D(m=10))) & Q(parking_type=ParkingType.FREE) & Q(is_transfer=False)        
                ).count()
        if exist > 0:
            self.errors['location'] = 'There is already a parking near you'
    
    def validate(self):
        self.validate_distance()
        return self.errors
    
