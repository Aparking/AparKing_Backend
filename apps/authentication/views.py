from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from apps.authentication.models import CustomUser
from rest_framework import status
from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, RegisterSerializer,UserSerializer

# Función auxiliar para verificar si el usuario es un administrador
def is_admin(user):
    # Verifica si el usuario está autenticado y si es un administrador (is_staff)
    return user.is_authenticated and user.is_staff

# Vista para listar y, opcionalmente, borrar usuarios
@api_view(['GET', 'POST', 'DELETE'])
# Decorador que restringe el acceso solo a los administradores
@user_passes_test(is_admin)
def users_list(request):
    if request.method == 'GET':
        # Obtiene todos los usuarios de la base de datos
        users = CustomUser.objects.all()
        
        # Filtra los usuarios por el nombre de usuario si se proporciona en la consulta
        username = request.GET.get('username', None)
        if username is not None:
            users = users.filter(username__icontains=username)
        
        # Serializa los usuarios encontrados
        users_serializer = UserSerializer(users, many=True)
        # Devuelve los datos de los usuarios serializados en forma de respuesta JSON
        return JsonResponse(users_serializer.data, safe=False)
    
    elif request.method == 'DELETE':
        # Elimina todos los usuarios de la base de datos
        count = CustomUser.objects.all().delete()
        # Devuelve un mensaje indicando cuántos usuarios se eliminaron con éxito
        return JsonResponse({'message': '{} Users were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
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
