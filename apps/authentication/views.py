from django.http import JsonResponse
from rest_framework.decorators import api_view
from apps.authentication.models import CustomUser
from rest_framework import status
from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
<<<<<<< HEAD
from rest_framework.parsers import JSONParser
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

    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Elimina todos los usuarios de la base de datos
        count = CustomUser.objects.all().delete()
        # Devuelve un mensaje indicando cuántos usuarios se eliminaron con éxito
        return JsonResponse({'message': '{} Users were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def users_detail(request, pk):
    try: 
        user = CustomUser.objects.get(pk=pk) 
    except CustomUser.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': 
        user_serializer = UserSerializer(user) 
        return JsonResponse(user_serializer.data)

    elif request.method == 'PUT': 
        user_data = JSONParser().parse(request) 
        user_serializer = UserSerializer(user, data=user_data) 
        if user_serializer.is_valid(): 
            user_serializer.save() 
            return JsonResponse(user_serializer.data) 
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE': 
        user.delete() 
        return JsonResponse({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
=======
from .serializers import CustomUserSerializer, LoginSerializer, RegisterSerializer,RegisterVehicleSerializer, ProfileSerializer
from apps.mailer import generic_sender as Mailer
from apps.utils import code_generator
import stripe
from apps.payment.models import MemberShip, CustomUser, Credit
from apps.authentication.models import Vehicle
from apps.payment.enums import MemberType
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from rest_framework import status
>>>>>>> f293d260ec4089ef07c2cc253cf94d8acfe4bc48

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
        customer = stripe.Customer.create(
            email = user.email,
            name = user.username
        )
        now = timezone.now()
        oneMonthLater = now + relativedelta(months=1)
        formattedNow = now.strftime('%Y-%m-%d %H:%M')
        formattedOneMonthLater = oneMonthLater.strftime('%Y-%m-%d %H:%M')
        memberShip=MemberShip(start_date=formattedNow,end_date=formattedOneMonthLater,type=MemberType.FREE,user=user)
        credit= Credit(value=50,creation_date=now ,user=user)
        memberShip.save()
        credit.save()
        user.stripe_customer_id = customer.id
        user.stripe_subscription_id = "price_1OzRzqC4xI44aLdHxKkbcfko"
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
    for vehiculo in Vehicle.objects.filter(owner=request.user.id):
        vehiculo.principalCar=False
        vehiculo.save()
    serializer = RegisterVehicleSerializer(data=datos)
    
    if serializer.is_valid():
        vehicle = serializer.save() 
        vehicle.principalCar= True
        vehicle.save()
        return Response(status=200)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(["PUT"])
def updateVehicle(request) -> Response:
    try:
        for vehiculo in Vehicle.objects.filter(owner=request.user.id):
            if vehiculo.id==request.data:
                vehicle= Vehicle.objects.get(id=vehiculo.id)
                vehicle.principalCar=True
                vehicle.save()
            else:
                vehicle= Vehicle.objects.get(id=vehiculo.id)
                vehicle.principalCar=False
                vehicle.save()
        return Response({'id': vehicle.id}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(["GET", "PUT", "DELETE"])
def user_profile(request):
    try:
        user = request.user

        if request.method == "GET":
            serializer = ProfileSerializer(user)
            return Response(serializer.data)

        elif request.method == "PUT":
            serializer = ProfileSerializer(user, data=request.data)
            print(serializer)
            if serializer.is_valid():
                print("funciona")
                serializer.save()
                return Response(serializer.data)
            else:
                print("hola")
                return Response(serializer.errors, status=400)
        elif request.method == "DELETE":
            user.delete()
            return Response(status=204)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 


