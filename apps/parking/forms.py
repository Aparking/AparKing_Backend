from django import forms
from django.contrib.gis import forms
from apps.parking.models import Parking, Size, ParkingType

class ParkingForm(forms.ModelForm):
    class Meta:
        model = Parking
        fields = '__all__'
