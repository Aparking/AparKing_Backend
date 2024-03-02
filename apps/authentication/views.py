from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from apps.authentication.models import CustomUser
from rest_framework import status
      
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, RegisterSerializer,UserSerializer

@api_view(['GET', 'POST', 'DELETE'])
def users_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        
        username = request.GET.get('username', None)
        if username is not None:
            users = users.filter(username__icontains=username)
        
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
    
    elif request.method == 'DELETE':
        count = CustomUser.objects.all().delete()
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
