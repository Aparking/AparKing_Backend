from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.garagement.models import Garage
from .models import Book, Availability
from .serializers import BookSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from apps.garagement.enums import GarageStatus
from apps.booking.enums import BookingStatus,PaymentMethod
from rest_framework.exceptions import ValidationError


import stripe
from django.conf import settings
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


stripe.api_key = settings.STRIPE_SECRET_KEY



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    data = request.data
    user = request.user
    availability = get_object_or_404(Availability, id=data['availability'])
    garage = get_object_or_404(Garage, id=availability.garage.id)
    availability.status = GarageStatus.RESERVED.value
    availability.save()

    book = Book.objects.create(
        payment_method=data.get('payment_method'),
        status=BookingStatus.CONFIRMED.value,
        user=user,
        availability=availability
    )
    book_serializer = BookSerializer(book)
    return Response(book_serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_my_bookings(request):
    user = request.user
    bookings = Book.objects.filter(user=user)
    if bookings.exists():
        serializer = BookSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'No se encontraron reservas de garajes.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_all_bookings(request):
    bookings = Book.objects
    if bookings.exists():
        serializer = BookSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'No se encontraron reservas de garajes.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def booking_details(request, pk):
    try:
        booking = get_object_or_404(Book, pk=pk)
        
        if request.method == "GET":
            serialized = BookSerializer(booking)
            return Response(serialized.data, status=status.HTTP_200_OK)

        elif request.method == "DELETE":
            booking.availability.status = GarageStatus.AVAILABLE.value
            booking.availability.save()
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response({"message": "No se encontró ninguna reserva para el garaje."}, status=status.HTTP_404_NOT_FOUND)
     
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    garage_id = request.data.get('garage')
    if not garage_id:
        return Response({'error': 'Se requiere un garaje para poner un comentario'}, status=status.HTTP_400_BAD_REQUEST)
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
    

    
@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    data = request.data
    user = request.user
    availability = get_object_or_404(Availability, id=data['availability'])
    

    book = Book.objects.create(
        payment_method=data.get('payment_method'),
        status=BookingStatus.PENDING.value,
        user=user,
        availability=availability
    )  
    try:
        succes='/garages'
        cancel= '/garages'
        amount = book.calculate_total_price()
        if(book.payment_method==str(PaymentMethod.CARD)):
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': f'Reserva de garaje {book.availability.garage.name}',
                            },
                            'unit_amount': int(amount*100),  
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=data['url']+ succes,
                    cancel_url=data['url']+ cancel,
                )
            book.stripe_session_id= session.id
            book.save()        
            return JsonResponse({'url': session.url, 'confirmacion': True})
        else:
            bookingStatus=BookingStatus.CONFIRMED.value,
            book.status=bookingStatus
            book.availability.status = GarageStatus.RESERVED.value
            book.availability.save()
            book.save()
            return JsonResponse({'url': data['url'], 'confirmacion': True})

    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e), 'confirmacion': False}, status=403)