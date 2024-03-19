from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Availability, Garage, Image, Address
from .serializers import *

from rest_framework import status, filters 
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

class GarageViewSet(ViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = {'price': ['lte', 'gte'],  'is_active': ['exact'], 'height': ['lte', 'gte'], 'width': ['lte', 'gte'], 'length': ['lte', 'gte'], 
                        'creation_date': ['lte', 'gte'], 'name':['contains'], 'address__country':['contains'], 'address__city':['contains'], 'address__region':['contains']}
    search_fields = ['name', 'address__country', 'address__city', 'address__region']
    ordering_fields = ['price', 'creation_date']
    ordering = ['creation_date']

    def listAllGarages(self, request):
        serializer = GarageSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    def listMyGarages(request):
        user = request.user
        user_garages = Garage.objects.filter(owner=user)
        if user_garages.exists():
            serializer = GarageSerializer(user_garages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'El usuario no tiene garajes propios.'}, status=status.HTTP_404_NOT_FOUND)
    
    def listGarages(self, request):
        if request.user.is_superuser:
            garages = Garage.objects.all()
        else:
            garages = Garage.objects.filter(availability__status='AVAILABLE', is_active=True)     
        if garages.exists():
            serializer = GarageSerializer(garages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No se encontraron garajes.'}, status=status.HTTP_404_NOT_FOUND)
    
    def listAvailableGarages(self, request):
        available_garages = Garage.objects.filter(availability__status='AVAILABLE', is_active=True)
        if available_garages.exists():
            serializer = GarageSerializer(available_garages, many=True)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No se encontraron garajes disponibles.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        garage_serializer = GarageSerializer(data=request.data)
        address_serializer = AddressSerializer(data=request.data["address"])
        # image_data = request.data.get("image", None)
        # image_serializer = ImageSerializer(data={'image': image_data} if image_data else None)
        if garage_serializer.is_valid() and address_serializer.is_valid():
            garage = garage_serializer.save()
            address_serializer.save()
            # if image_data:
            #     image = image_serializer.save()
            #     image.garage = garage
            # else:
            #     image = None
            data = {
                'garage': garage_serializer.data,
                'address': address_serializer.data,
                # 'image': image_serializer.data if image else None,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({
            'garage_errors': garage_serializer.errors,
            'address_errors': address_serializer.errors,
            # 'image_errors': image_serializer.errors if image_data else None
        }, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        garage = get_object_or_404(self.queryset, pk=pk)
        garage_images = Image.objects.filter(garage=garage)
        garage_address = Address.objects.get(pk=garage.address.id)
        garage_availability = Availability.objects.filter(garage=garage)

        garage_serializer = GarageSerializer(garage)
        garage_images_serializer = ImageSerializer(garage_images, many=True)
        garage_address_serializer = AddressSerializer(garage_address)
        garage_availability_serializer = AvailabilitySerializer(
            garage_availability, many=True
        )

        garage_data = garage_serializer.data
        garage_data["images"] = garage_images_serializer.data
        garage_data["address"] = garage_address_serializer.data
        garage_data["availability"] = garage_availability_serializer.data

        return Response(garage_data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        garage = get_object_or_404(self.queryset, pk=pk)
        serializer = GarageSerializer(garage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        garage = get_object_or_404(self.queryset, pk=pk)
        garage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class GarageListCreateAPIView(ListCreateAPIView):
#     queryset = Garage.objects.all()
#     serializer_class = GarageSerializer

#     def post(self, request):

#         if request.user.is_anonymous:
#             return Response(
#                 {"error": "You must be logged in to create a garage"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         # Extracting required data from the request
#         garage_data = {
#             "garage": request.data.get("garage"),
#             "address": request.data.get("address"),
#             "image": request.data.get("image"),
#         }

#         address = Address.objects.create(
#             street_number=garage_data["address"]["street_number"],
#             unit_number=garage_data["address"]["unit_number"],
#             address_line=garage_data["address"]["address_line"],
#             city=garage_data["address"]["city"],
#             region=garage_data["address"]["region"],
#             country=garage_data["address"]["country"],
#             postal_code=garage_data["address"]["postal_code"],
#         )

#         # Creating garage object

#         garage = Garage.objects.create(
#             name=garage_data["garage"]["name"],
#             description=garage_data["garage"]["description"],
#             height=garage_data["garage"]["height"],
#             width=garage_data["garage"]["width"],
#             length=garage_data["garage"]["length"],
#             price=garage_data["garage"]["price"],
#             creation_date=garage_data["garage"]["creation_date"],
#             modification_date=garage_data["garage"]["modification_date"],
#             is_active=garage_data["garage"]["is_active"],
#             owner=request.user,
#             address=address,
#         )

#         # Creating image object associated with the garage
#         image = Image.objects.create(
#             image=garage_data["image"]["image_url"],
#             alt=garage_data["image"]["alt"],
#             publication_date=garage_data["image"]["publication_date"],
#             garage=garage,
#         )

#         # Serializing garage and image objects
#         garage_serialized = GarageSerializer(garage)
#         image_serialized = ImageSerializer(image)

#         # Returning response with serialized data
#         return Response(
#             {"garage": garage_serialized.data, "image": image_serialized.data},
#             status=status.HTTP_201_CREATED,
#         )


# class GarageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Garage.objects.all()
#     serializer_class = GarageSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsAdminUser]


# class ImageListCreateAPIView(ListCreateAPIView):
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
#     permission_classes = [IsAuthenticated]


# class ImageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsAdminUser]


# class AvailabilityListCreateAPIView(ListCreateAPIView):
#     queryset = Availability.objects.all()
#     serializer_class = AvailabilitySerializer
#     permission_classes = [IsAuthenticated]


# class AvailabilityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Availability.objects.all()
#     serializer_class = AvailabilitySerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsAdminUser]


# class AvailableGaragesListAPIView(ListCreateAPIView):
#     serializer_class = GarageSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         available_availabilities = Availability.objects.filter(status="AVAILABLE")
#         return [availability.garage for availability in available_availabilities]


# class MyGaragesListAPIView(ListCreateAPIView):
#     queryset = Garage.objects.all()
#     serializer_class = GarageSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.filter(owner=self.request.user)


# class MyAvailableGaragesListAPIView(ListCreateAPIView):
#     serializer_class = GarageSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         available_availabilities = Availability.objects.filter(
#             status="AVAILABLE", owner=self.request.user
#         )
#         return [availability.garage for availability in available_availabilities]
