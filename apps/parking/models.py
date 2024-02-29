from django.db import models

from django.contrib.gis.db import models as gis_models

from apps.authentication.models import CustomUser
from apps.parking.enums import Size

class Parking(models.Model):
    size = models.CharField(max_length=16, choices=Size.choices(), blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    location = gis_models.PointField(blank=False, null=False)
    is_transfer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    is_assignment = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
   
    class Meta:
        verbose_name = "Aparcamiento"
        verbose_name_plural = "Aparcamientos"
