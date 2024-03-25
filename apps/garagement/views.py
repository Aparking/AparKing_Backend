from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Image, Garage
from .serializers import GarageSerializer, ImageSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_garage(request):
    if request.method == "POST":
        garage_serializer = GarageSerializer(data=request.data)
        garage_valid = garage_serializer.is_valid()

        if garage_valid:
            garage_serializer.save()
            return Response(garage_serializer.data, status=status.HTTP_201_CREATED)
        else:
            errors = {}
            if not garage_valid:
                errors.update(garage_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_image(request):
    if request.method == "POST":
        image_serializer = ImageSerializer(data=request.data)
        image_valid = image_serializer.is_valid()
        if image_valid:
            image_serializer.save()
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            errors = {}
            if not image_valid:
                errors.update(image_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_image(request):
    if request.method == "GET":
        serializer = ImageSerializer(Image.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_my_garages(request):
    if request.method == "GET":
        user = request.user
        garages = Garage.objects.filter(owner=user)
        if garages.exists():
            serializer = GarageSerializer(garages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "No se encontraron garajes."},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET"])
def list_garages(request):
    if request.method == "GET":
        user = request.user
        if user.is_superuser:
            garages = Garage.objects.all()
        else:
            garages = Garage.objects.filter(is_active=True)

        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        min_height = request.query_params.get("min_height")
        max_height = request.query_params.get("max_height")
        min_width = request.query_params.get("min_width")
        max_width = request.query_params.get("max_width")
        min_length = request.query_params.get("min_length")
        max_length = request.query_params.get("max_length")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        name_contains = request.query_params.get("name")
        city = request.query_params.get("city")
        region = request.query_params.get("region")
        country = request.query_params.get("country")
        postal_code = request.query_params.get("postal_code")

        if min_price is not None:
            garages = garages.filter(price__gte=min_price)
        if max_price is not None:
            garages = garages.filter(price__lte=max_price)
        if min_height is not None:
            garages = garages.filter(height__gte=min_height)
        if max_height is not None:
            garages = garages.filter(height__lte=max_height)
        if min_width is not None:
            garages = garages.filter(width__gte=min_width)
        if max_width is not None:
            garages = garages.filter(width__lte=max_width)
        if min_length is not None:
            garages = garages.filter(length__gte=min_length)
        if max_length is not None:
            garages = garages.filter(length__lte=max_length)
        if start_date is not None:
            garages = garages.filter(creation_date__gte=start_date)
        if end_date is not None:
            garages = garages.filter(creation_date__lte=end_date)
        if name_contains is not None:
            garages = garages.filter(name__icontains=name_contains)
        if city is not None:
            garages = garages.filter(address__city__icontains=city)
        if region is not None:
            garages = garages.filter(address__region__icontains=region)
        if country is not None:
            garages = garages.filter(address__country__iexact=country)
        if postal_code is not None:
            garages = garages.filter(address__postal_code__iexact=postal_code)

        garages = garages.order_by("price", "creation_date")
        if garages.exists():
            serializer = GarageSerializer(garages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "No se encontraron garajes."},
                status=status.HTTP_404_NOT_FOUND,
            )
