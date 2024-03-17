
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.authentication.models import CustomUser

from .enums import GarageStatus
from .models import Availability, Garage, Image, Address
from .serializers import AvailabilitySerializer, GarageSerializer, ImageSerializer
from rest_framework.decorators import api_view

from rest_framework import status
from rest_framework.response import Response


class GarageListCreateAPIView(ListCreateAPIView):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    
    def post(self, request):

            if request.user.is_anonymous:
                return Response(
                    {"error": "You must be logged in to create a garage"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Extracting required data from the request
            garage_data = {
                "garage": request.data.get("garage"),
                "address": request.data.get("address"),
                "image": request.data.get("image"),
            }

            address = Address.objects.create(
                street_number=garage_data["address"]["street_number"],
                unit_number=garage_data["address"]["unit_number"],
                address_line=garage_data["address"]["address_line"],
                city=garage_data["address"]["city"],
                region=garage_data["address"]["region"],
                country=garage_data["address"]["country"],
                postal_code=garage_data["address"]["postal_code"],
            )

            # Creating garage object
            ivan= CustomUser.objects.get(username="ivan")
            garage = Garage.objects.create(
                
                name = garage_data["garage"]["name"],
                description = garage_data["garage"]["description"],
                height = garage_data["garage"]["height"],
                width = garage_data["garage"]["width"],
                length = garage_data["garage"]["length"],
                price = garage_data["garage"]["price"],
                creation_date = garage_data["garage"]["creation_date"],
                modification_date = garage_data["garage"]["modification_date"],
                is_active = garage_data["garage"]["is_active"],
                owner = ivan,
                address = address,


            )

            # Creating image object associated with the garage
            image = Image.objects.create(
                image=garage_data["image"]["image_url"],
                alt=garage_data["image"]["alt"],
                publication_date=garage_data["image"]["publication_date"],
                garage=garage,
            )

            # Serializing garage and image objects
            garage_serialized = GarageSerializer(garage)
            image_serialized = ImageSerializer(image)

            # Returning response with serialized data
            return Response(
                {"garage": garage_serialized.data, "image": image_serialized.data},
                status=status.HTTP_201_CREATED,
            )
    
    
class GarageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    
class ImageListCreateAPIView(ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
class ImageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
class AvailabilityListCreateAPIView(ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    
class AvailabilityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    
class AvailableGaragesListAPIView(ListCreateAPIView):
    serializer_class = GarageSerializer

    def get_queryset(self):
        available_availabilities = Availability.objects.filter(status=GarageStatus.AVAILABLE)
        return [availability.garage for availability in available_availabilities]
    
class MyGaragesListAPIView(ListCreateAPIView):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class MyAvailableGaragesListAPIView(ListCreateAPIView):
    serializer_class = GarageSerializer

    def get_queryset(self):
        available_availabilities = Availability.objects.filter(status=GarageStatus.AVAILABLE, owner=self.request.user)
        return [availability.garage for availability in available_availabilities]

