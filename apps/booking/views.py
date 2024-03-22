from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from AparKing_Backend.apps.booking.enums import BookingStatus
from apps.booking.models import Book
from apps.booking.serializers import CommentSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    garage_id = request.data.get('garage_id')
    user = request.user

    finished_bookings = Book.objects.filter(
        user=user,
        availability__garage_id=garage_id,
        availability__end_date__lt=make_aware(datetime.now()),  
        status=BookingStatus.choices().CONFIRMED.value
    )

    if not finished_bookings.exists():
        return Response({'error': 'No se encontraron reservas confirmadas y finalizadas para este garaje por el usuario.'}, status=status.HTTP_400_BAD_REQUEST)

    comment_serializer = CommentSerializer(data=request.data)
    if comment_serializer.is_valid():
        comment_serializer.save(user=user, garage_id=garage_id)
        return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)