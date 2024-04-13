from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from apps.garagement.models import Garage
from .models import Book, Availability
from .serializers import BookSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from apps.garagement.enums import GarageStatus
from apps.booking.enums import BookingStatus
from rest_framework.exceptions import ValidationError
from django.utils.timezone import make_aware

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_booking(request):
    if request.method == "POST":
        book_serializer = BookSerializer(data=request.data)
        if book_serializer.is_valid():
            availability_id = request.data.get('availability')
            try:
                availability = Availability.objects.get(id=availability_id)
            except Availability.DoesNotExist:
                return Response({"error": "La disponibilidad especificada no existe."}, status=status.HTTP_404_NOT_FOUND)
            if availability.status == GarageStatus.RESERVED.value:
                return Response({"error": "Ya existe una reserva para esta disponibilidad."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                availability.status = GarageStatus.RESERVED.value
                availability.save()
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
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    garage_id = request.data.get('garage_id')
    user = request.user

    finished_bookings = Book.objects.filter(
        user=user,
        availability__garage_id=garage_id,
        availability__end_date__lt=make_aware(datetime.now()),
        status=BookingStatus.CONFIRMED.value
    )

    if not finished_bookings.exists():
        return Response({'error': 'No se encontraron reservas confirmadas y finalizadas para este garaje por el usuario.'}, status=status.HTTP_400_BAD_REQUEST)

    comment_serializer = CommentSerializer(data=request.data)
    if comment_serializer.is_valid():
        comment_serializer.save(user=user, garage_id=garage_id)
        return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)