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
from rest_framework.exceptions import ValidationError

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_booking(request):
    if request.method == "POST":
        book_serializer = BookSerializer(data=request.data)
        if book_serializer.is_valid():
            availability_id = request.data.get('availability')
            availability = Availability.objects.get(id=availability_id)
            if availability.status == GarageStatus.RESERVED.value:
                raise ValidationError("Ya existe una reserva para este garaje.")
            else:
                book_serializer.save()
                return Response(book_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_my_bookings(request):
    if request.method == "GET":
        user = request.user
        bookings = Book.objects.filter(user=user)
        if bookings.exists():
            serializer = BookSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No se encontraron reservas de garajes."}, status=status.HTTP_404_NOT_FOUND)
            
@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def booking_details(request, pk):
    try:
        booking = Book.objects.get(pk=pk)
        if request.method == "GET":
            serialized = BookSerializer(booking)
            return Response(serialized.data, status=status.HTTP_200_OK)

        elif request.method == "DELETE":
            availability = booking.availability
            availability.status = GarageStatus.AVAILABLE.value
            availability.save()
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response({"message": "No se encontró ninguna reserva para el garaje."}, status=status.HTTP_404_NOT_FOUND)