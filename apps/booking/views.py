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

import stripe
from django.conf import settings
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


stripe.api_key = settings.STRIPE_SECRET_KEY



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
    
@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    data = json.loads(request.body.decode('utf-8'))
    
    try:
        booking_id = data
        booking = Book.objects.get(id=booking_id)
        amount = booking.calculate_total_price
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'Reserva de garaje {booking.availability.garage.name}',
                        },
                        'unit_amount': amount*100,  
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8100/bookings/',
                cancel_url='http://localhost:8100',
            )
        
        return JsonResponse({'url': session.url, 'confirmacion': True})

    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e), 'confirmacion': False}, status=403)