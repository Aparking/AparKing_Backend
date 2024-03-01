from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from channels.layers import get_channel_layer

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.http import HttpRequest
from django.shortcuts import render
from django.db.models import Q

from apps.parking.models import Parking, ParkingType
from apps.parking.forms import ParkingForm
from apps.parking.serializers import ParkingSerializer
from apps.parking.filters import ParkingFilter
from apps.parking.coordenates import Coordenates
from apps.parking.validators import ParkingValidator


channel_layer = get_channel_layer()

# Create your views here.
def index(request):
    return render(request, "parking/index.html")

def room(request, room_name):
    return render(request, "parking/room.html", {"room_name": room_name})

@api_view(['POST'])
def get_parking_near(request: HttpRequest):
    filter = ParkingFilter.from_request(request)
    near = filter.get_queryset()
    serializer = ParkingSerializer(near, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_parking(request: HttpRequest):
    data = request.POST.copy()
    coordenates = Coordenates.from_request(request)
    data["location"] = coordenates.get_point() 
    form = ParkingForm(data)
    if form.is_valid():
        errors = ParkingValidator(form).validate()
        if len(errors) > 0:
            return Response({'error': errors}, status=status.HTTP_409_CONFLICT)
        parking = form.save()
        serializer = ParkingSerializer(parking, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)


