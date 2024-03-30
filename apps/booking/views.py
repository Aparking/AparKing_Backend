from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from apps.garagement.models import Garage
from .models import Book, Availability
from .serializers import BookSerializer
from django.shortcuts import get_object_or_404
from apps.garagement.enums import GarageStatus
from apps.booking.enums import BookingStatus

        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    if request.method == 'POST':
        data = request.data
        user = request.user
        availability = get_object_or_404(Availability, id=data['availability'])
        garage = get_object_or_404(Garage, id=availability.garage.id)
        availability.status = GarageStatus.RESERVED.value
        availability.save()

        book = Book.objects.create(payment_method=data['payment_method'], status=BookingStatus.CONFIRMED.value, user=user, availability=availability)
        bookSerializer = BookSerializer(book)
        bookSerializer.save()
        return Response(bookSerializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_my_bookings(request):
    if request.method == 'GET':
        user = request.user
        bookings = Book.objects.filter(user=user)
        if bookings.exists():
            serializer = BookSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No se encontraron reservas de garajes.'}, status=status.HTTP_404_NOT_FOUND)
         
@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def booking_details(request, pk):
    try:
        booking = Book.objects.get(pk=pk)
    except booking.DoesNotExist:
        return Response({"message": "No se encontró ninguna reserva para el garaje."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serialized = BookSerializer(booking)
        return Response(serialized.data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        booking.availability.status = GarageStatus.AVAILABLE.value
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)