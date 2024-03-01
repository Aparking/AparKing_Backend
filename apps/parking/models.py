#from django.db import models
from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

from enumchoicefield import EnumChoiceField
from enum import Enum

from apps.authentication.models import CustomUser
# Create your models here.

class ParkingType(Enum):
    ASSIGNMENT = "ASSIGNMENT"
    FREE = "FREE"
    PRIVATE = "PRIVATE"

class ParkingSize(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    

class City(models.Model):
    name = models.CharField(null=False, blank=False)
    name_ascii = models.CharField(null=True, blank=True)
    alternative_name = models.TextField(null=True, blank=True)
    location = models.PointField(srid=4326, null=False, blank=False)
    country_code = models.CharField(null=True, blank=False)


class Parking(models.Model):
    notified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    booked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(blank = True, null=True)
    location = models.PointField(srid=4326)
    size = EnumChoiceField(ParkingSize, default=ParkingSize.MEDIUM, null=False, blank=False)
    is_asignment = models.BooleanField(default = False, null=False, blank=False)
    is_transfer = models.BooleanField(default = False, null=False, blank=False)
    parking_type = EnumChoiceField(ParkingType, default=ParkingType.FREE, null=False, blank=False) 

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update date")
    
    class Meta:
        verbose_name = "Aparcamiento"
        verbose_name_plural = "Aparcamientos"

    def get_lat_long(self):
        latitud = self.location.y
        longitud = self.location.x
        return latitud, longitud

    def __str__(self):
        return str(self.location.x) +" " + str(self.location.y)
    

