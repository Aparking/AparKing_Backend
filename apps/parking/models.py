from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from enumchoicefield import EnumChoiceField
from apps.authentication.models import CustomUser,Vehicle
from apps.parking.enums import Size, ParkingType

class City(models.Model):
    name = models.CharField(null=False, blank=False)
    name_ascii = models.CharField(null=True, blank=True)
    alternative_name = models.TextField(null=True, blank=True)
    location = models.PointField(srid=4326, null=False, blank=False)
    country_code = models.CharField(null=True, blank=False)

class Parking(models.Model):
    notified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="parking_notified_by")
    booked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="parking_booked_by")
    message = models.CharField(blank = True, null=True)
    location = models.PointField(srid=4326)
    size = EnumChoiceField(Size, default=Size.SUV, null=False, blank=False)
    is_assignment = models.BooleanField(default = False, null=False, blank=False)
    is_transfer = models.BooleanField(default = False, null=False, blank=False)
    parking_type = EnumChoiceField(ParkingType, default=ParkingType.FREE, null=False, blank=False) 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update date")
    cesion_parking = models.DateTimeField(null=True, blank=True, verbose_name="Cesion parking")
    vehiculo=models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True, related_name="parking_vehicle")
    
    class Meta:
        verbose_name = "Aparcamiento"
        verbose_name_plural = "Aparcamientos"

    def get_lat_long(self):
        latitud = self.location.y
        longitud = self.location.x
        return latitud, longitud

    def __str__(self):
        return str(self.location.x) +" " + str(self.location.y)

    def to_json(self):
        
        return {
            'id': self.id,
            'notified_by': self.notified_by_id,  
            'booked_by': self.booked_by_id,      
            'location': str(self.location),       
            'message': self.message,
            'size': self.size.label,              
            'is_assignment': self.is_assignment,
            'is_transfer': self.is_transfer,
            'parking_type': self.parking_type.label,  
            'created_at': self.created_at.isoformat(), 
            'updated_at': self.updated_at.isoformat(),
            'cesion_parking': self.cesion_parking.isoformat(),
        }
    

