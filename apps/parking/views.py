from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.db.models import Q

from apps.parking.models import Parking, City
from apps.parking.enums import ParkingType, ParkingSize, NoticationsSocket
from apps.parking.forms import ParkingForm
from apps.parking.serializers import ParkingSerializer
from apps.parking.filters import ParkingFilter
from apps.parking.coordenates import Coordenates
from apps.parking.validators import ParkingValidator

from django.contrib.auth.decorators import login_required

channel_layer = get_channel_layer()


def manage_send_parking_created(type: str, message: dict, coordenates: Point):
    city_near = City.objects.annotate(distance=Distance('location', coordenates)).order_by('distance').first()
    if city_near:
        group: str = f"{city_near.location.y}_{city_near.location.x}"
        async_to_sync(channel_layer.group_send)(
                group, {"type": type, "message": message}
            )

# Create your views here.
def index(request):
    return render(request, "parking/index.html")

def room(request, room_name):
    return render(request, "parking/room.html", {"room_name": room_name})

@api_view(['POST'])
@login_required
def get_parking_near(request: HttpRequest):
    filter_parking = ParkingFilter.from_request(request)
    near = filter_parking.get_queryset()
    coordenates = Coordenates.from_request(request)
    city_near = City.objects.annotate(distance=Distance('location', coordenates.get_point())).order_by('distance').first()
    serializer = ParkingSerializer(near, many=True).data
    group: str = f"{city_near.location.y}_{city_near.location.x}"
    serializer.append({'group': group})
    return Response(serializer, status=status.HTTP_200_OK)

@api_view(['POST'])
@login_required
def create_parking(request: HttpRequest):
    serializer = ParkingSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        parking_instance = Parking(**validated_data)
        errors = ParkingValidator(parking_instance).validate()
        if len(errors) > 0:
            return Response({'error': errors}, status=status.HTTP_409_CONFLICT)
        parking = serializer.save(notified_by=request.user)
        manage_send_parking_created(NoticationsSocket.PARKING_NOTIFIED.value, ParkingSerializer(parking).data, parking.location)
        return JsonResponse({'id': parking.id}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@login_required
def assign_parking(request: HttpRequest, parking_id: int):
    try:
        parking = Parking.objects.get(pk=parking_id, is_asignment=False)
        parking.is_asignment = True
        parking.booked_by = request.user
        parking.save()
        manage_send_parking_created(NoticationsSocket.PARKING_BOOKED.value, parking.id, parking.location)
        return JsonResponse({"message": "Parking assigned"}, status=200)
    except Parking.DoesNotExist:
        return JsonResponse({"message": "The parking doesn't exist"}, status=404)

@api_view(['PUT'])
@login_required
def transfer_parking(request: HttpRequest, parking_id: int):
    try:
        parking = Parking.objects.get(pk=parking_id, is_asignment=True, parking_type=ParkingType.ASSIGNMENT, is_transfer=False, notified_by=request.user)
        parking.is_transfer = True
        parking.save()
        return JsonResponse({"message": "Parking assigned"}, status=200)
    except Parking.DoesNotExist:
        return JsonResponse({"message": "The parking doesn't exist"}, status=404)
    
@api_view(['DELETE'])
@login_required
def delete_parking(request: HttpRequest, parking_id: int):
    try:
        parking = Parking.objects.get(pk=parking_id, is_asignment=False, notified_by=request.user)
        manage_send_parking_created(NoticationsSocket.PARKING_DELETED.value, parking.id, parking.location)
        parking.delete()
        return JsonResponse({"message": "Parking deleted"}, status=200)
    except Parking.DoesNotExist:
        return JsonResponse({"message": "The parking doesn't exist"}, status=404)