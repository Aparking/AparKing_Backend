from django.http import JsonResponse
from rest_framework.decorators import api_view
from apps.authentication.models import CustomUser
from rest_framework import status
from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import CustomUserSerializer, LoginSerializer, RegisterSerializer,RegisterVehicleSerializer
from apps.mailer import generic_sender as Mailer
from apps.utils import code_generator
from apps.authentication.models import CustomUser


@api_view(["POST"])
def auth_login(request) -> Response:
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        Token.objects.filter(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)
    else:
        return Response(serializer.errors, status=400)


@api_view(["POST"])
def delete_account(request) -> Response:
    try:
        token = Token.objects.get(key=request.data["token"])
        if token:
            user = token.user
            user.delete()
            return Response(status=200)
        else:
            return Response(status=400)
    except Exception:
        return Response(status=400)


@api_view(["POST"])
def verify_user(request) -> Response:
    try:
        token = Token.objects.get(key=request.data["token"])
        if token:
            user = token.user
            if user.code == request.data["code"]:
                user.is_active = True
                user.save()
                token.delete()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=400)
    except Exception:
        return Response({"error": "Token not found"}, status=400)


@api_view(["GET"])
def user_info(request) -> Response:
    user = request.user
    if user.is_authenticated:
        custom_user = CustomUser.objects.get(id=user.id)
        serialized = CustomUserSerializer(custom_user)
        return Response(serialized.data, status=200)
    return Response(status=401)


@api_view(["POST"])
def register(request) -> Response:
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False
        user.code = code_generator.code_generator(10)
        token, _ = Token.objects.get_or_create(user=user)
        Mailer.send_email(
            subject="AparKing - Activar cuenta",
            message=f"Bienvenido {user.first_name}, para activar su cuenta introduzca el siguiente código: {user.code}",
            mail_to=user.email,
        )
        user.save()
        return Response({"token": token.key}, status=200)
    else:
        return Response(serializer.errors, status=400)


@api_view(["GET"])
def auth_logout(request) -> Response:
    user = request.user
    if user.is_authenticated:
        Token.objects.filter(user=user).delete()
        return Response(status=200)
    return Response(status=401)


@api_view(["POST"])
def registerVehicle(request) -> Response:
    datos = request.data.copy()
    datos['owner'] = request.user.id
    print(datos)
    serializer = RegisterVehicleSerializer(data=datos)
    print(serializer)
    if serializer.is_valid():
        vehicle = serializer.save() 
        vehicle.save()
        return Response(status=200)
    else:
        return Response(serializer.errors, status=400)

