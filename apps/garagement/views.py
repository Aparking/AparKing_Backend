from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .enums import GarageStatus
from .models import Availability, Garage, Image
from .serializers import AvailabilitySerializer, GarageSerializer, ImageSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, permission_classes

# GARAGE VIEWS

class GarageListCreateAPIView(ListCreateAPIView):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    permission_classes = [IsAuthenticated]
    
    #TODO - Custom garage create method to include images
    # def post(self, request):
    #     pass  
    
class GarageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsAdminUser]
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_images_by_garage(request, pk):
    try:
        images = Image.objects.filter(garage=pk)
    except NotFound:
        return Response({'error': 'Images not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data)

# IMAGE VIEWS

class ImageListCreateAPIView(ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    
class ImageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsAdminUser]
    
class AvailabilityListCreateAPIView(ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]
    
class AvailabilityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsAdminUser]