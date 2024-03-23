from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Image, Garage
from .serializers import GarageSerializer, ImageSerializer

@api_view(['POST'])
def create_garage(request):
    if request.method == 'POST':
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
        
@api_view(['POST'])
def create_image(request):
    if request.method == 'POST':
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


@api_view(['GET'])
def list_image(request):
    if request.method == 'GET':
        serializer = ImageSerializer(Image.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def list_garage(request):
    if request.method == 'GET':
        serializer = GarageSerializer(Garage.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)