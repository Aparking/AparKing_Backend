from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from .serializers import LoginSerializer, RegisterSerializer

@api_view(['POST'])
def auth_login(request) -> Response:
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=201)
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def register(request) -> Response:
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=201)
    else:
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def auth_logout(request) -> Response:
    user = request.user
    if user.is_authenticated:
        # Invalidar cualquier token asociado con el usuario
        Token.objects.filter(user=user).delete()
        return Response({'status': 'success'})
    return Response(status=401)
