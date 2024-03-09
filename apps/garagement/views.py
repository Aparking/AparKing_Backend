from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .enums import GarageStatus
from .models import Availability, Garage, Image
from .serializers import AvailabilitySerializer, GarageSerializer, ImageSerializer
from .permissions import IsOwnerOrReadOnly


class GarageListCreateAPIView(ListCreateAPIView):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    permission_classes = [IsAuthenticated]
    
class GarageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsAdminUser]
    
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
    
class AvailableGaragesListAPIView(ListCreateAPIView):
    serializer_class = GarageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        available_availabilities = Availability.objects.filter(status="AVAILABLE")
        return [availability.garage for availability in available_availabilities]
    
class MyGaragesListAPIView(ListCreateAPIView):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class MyAvailableGaragesListAPIView(ListCreateAPIView):
    serializer_class = GarageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        available_availabilities = Availability.objects.filter(status="AVAILABLE", owner=self.request.user)
        return [availability.garage for availability in available_availabilities]

