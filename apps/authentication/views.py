from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, RegisterSerializer

@api_view(['POST'])
def auth_login(request) -> Response:
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        login(request, user)
        return Response({'status': 'success'})
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def register(request) -> Response:
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({'status': 'success'})
    else:
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def auth_logout(request) -> Response:
    logout(request)
    return Response({'status': 'success'})
