from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Availability, Garage, Image, Address
from .serializers import *

from rest_framework import status
from rest_framework.response import Response


class GarageViewSet(ViewSet):
    queryset = Garage.objects.all()

    def list(self, request):
        serializer = GarageSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        try:
            garage = Garage.objects.get(pk=pk)
            garage.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Garage.DoesNotExist:
            return Response({"error": "Garaje no encontrado"}, status=status.HTTP_404_NOT_FOUND)


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
