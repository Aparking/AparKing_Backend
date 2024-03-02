from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Availability, Garage, Image
from .serializers import AvailabilitySerializer, GarageSerializer, ImageSerializer


class GarageListCreateAPIView(ListCreateAPIView):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    #permission_classes = [IsAuthenticated]

class ImageListCreateAPIView(ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    #permission_classes = [IsAuthenticated]
    
class AvailabilityListCreateAPIView(ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    #permission_classes = [IsAuthenticated]
