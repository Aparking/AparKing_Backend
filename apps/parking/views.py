from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.db.models import Q

from apps.parking.models import Parking, City
from apps.parking.enums import ParkingType, NoticationsSocket, Size
from apps.parking.serializers import ParkingSerializer
from apps.parking.filters import ParkingFilter
from apps.parking.coordenates import Coordenates

from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated

import logging

logger = logging.getLogger(__name__)



def manage_send_parking_created(type: str, message: dict, coordenates: Point):
    city_near = City.objects.annotate(distance=Distance('location', coordenates)).order_by('distance').first() 
    group: str = f"{city_near.location.y}_{city_near.location.x}".replace('.', 'p').replace('-', 'm') if city_near else "withoutData"
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        group,
        {
                "type": type,
                "message": message
            }
        )

       
        
    except Exception as e:
        raise e

def index(request):
    return render(request, "parking/index.html")

def room(request, room_name):
    return render(request, "parking/room.html", {"room_name": room_name})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_parking_near(request: HttpRequest):
    """
    Obtiene los aparcamientos cercanos a las coordenadas proporcionadas en la solicitud.

    Esta función espera una solicitud POST que incluya coordenadas de latitud y longitud. Basándose en estas coordenadas, busca en la base de datos los aparcamientos cercanos y los devuelve.

    Parámetros:
    - request (HttpRequest): La solicitud HTTP. Debe contener un cuerpo JSON con la latitud y longitud desde donde buscar aparcamientos cercanos.

    Retorna:
    - Response: Una respuesta HTTP con un código de estado 200 y un JSON que contiene los aparcamientos cercanos y el grupo de notificación asociado, o un mensaje de error si se produce algún fallo.

    Ejemplo de cuerpo de solicitud JSON esperado:
    ```json
    {
        "latitude": 42.3851,
        "longitude": 2.1734
    }
    ```
    """
    filter_parking = ParkingFilter.from_request(request)
    if not filter_parking:
        return JsonResponse({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    near = filter_parking.get_queryset()
    coordenates = Coordenates.from_request(request)
    city_near = City.objects.annotate(distance=Distance('location', coordenates.get_point())).order_by('distance').first()
    if not city_near:
        return Response({'error': 'No city found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ParkingSerializer(near, many=True).data
    group: str = f"{city_near.location.y}_{city_near.location.x}".replace('.', 'p').replace('-', 'm') if city_near else "withoutData"
    res = {'group': group, 'parkingData': serializer}
    return Response(res, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_parking(request: HttpRequest):
    """
    Crea un nuevo aparcamiento y lo notifica a los usuarios cercanos.

    Esta función espera una solicitud POST con un cuerpo JSON que describe el nuevo aparcamiento. El aparcamiento se crea basado en los datos proporcionados y se notifica a los usuarios cercanos sobre su disponibilidad.

    Parámetros:
    - request (HttpRequest): La solicitud HTTP. Debe contener un cuerpo JSON con la ubicación, el tamaño y el tipo de aparcamiento.

    Retorna:
    - JsonResponse: En caso de éxito, retorna un JsonResponse con el ID del aparcamiento creado. Si falla la validación o surge algún error, retorna un mensaje de error.

    Ejemplo de cuerpo de solicitud JSON esperado:
    ```json
    {
        "location": {
            "type": "Point",
            "coordinates": [42.3851, 2.1734]
        },
        "size": "MEDIUM",
        "parking_type": "FREE"
    }
    ```

    Campos del JSON:
    - location (dict): Un objeto que especifica el tipo de geometría ('Point') y las coordenadas del punto (latitud, longitud).
    - size (str): El tamaño del aparcamiento, que puede ser "SMALL", "MEDIUM" o "LARGE".
    - parking_type (str): El tipo de aparcamiento, que puede ser "FREE" o "ASSIGNMENT".

    Nota: Las coordenadas se deben proporcionar en el orden [latitud, longitud].
    """
    data = request.data
   # data["notified_by"] = request.user.id
    serializer = ParkingSerializer(data=data)
    if serializer.is_valid():
        parking = serializer.save()
        manage_send_parking_created(NoticationsSocket.PARKING_NOTIFIED.value, ParkingSerializer(parking).data, parking.location)
        return JsonResponse({'id': parking.id}, status=status.HTTP_201_CREATED)
    else:
        print('serializer:',serializer.errors)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def assign_parking(request: HttpRequest, parking_id: int):
    """
    Asigna un aparcamiento a un usuario.

    Esta función espera una solicitud PUT con el ID del aparcamiento a asignar. Si el aparcamiento está disponible (no asignado), lo asigna al usuario que hace la solicitud.

    Parámetros:
    - request (HttpRequest): La solicitud HTTP.
    - parking_id (int): El ID del aparcamiento a asignar.

    Retorna:
    - JsonResponse: En caso de éxito, retorna un JsonResponse con un mensaje de confirmación. Si el aparcamiento ya está asignado o no existe, retorna un mensaje de error.

    Ejemplo de uso:
    Para asignar un aparcamiento, se debe enviar una solicitud PUT a '/assign/{parking_id}', donde '{parking_id}' es el ID del aparcamiento a asignar.
    """
    try:
        parking = Parking.objects.get(pk=parking_id, is_assignment=False)
        parking.is_assignment = True
        #parking.booked_by = request.user
        parking.save()
        manage_send_parking_created(NoticationsSocket.PARKING_BOOKED.value, ParkingSerializer(parking).data, parking.location)
        return JsonResponse({"message": "Parking assigned"}, status=200)
    except Parking.DoesNotExist:
        return JsonResponse({"message": "The parking doesn't exist"}, status=404)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def transfer_parking(request: HttpRequest, parking_id: int):
    """
    Transfiere un aparcamiento asignado a otro usuario.

    Esta función permite a un usuario que ha asignado previamente un aparcamiento transferirlo a otro usuario. Espera una solicitud PUT con el ID del aparcamiento a transferir.

    Parámetros:
    - request (HttpRequest): La solicitud HTTP.
    - parking_id (int): El ID del aparcamiento a transferir.

    Retorna:
    - JsonResponse: En caso de éxito, retorna un JsonResponse con un mensaje de confirmación. Si el aparcamiento no está asignado, no es transferible, o no existe, retorna un mensaje de error.

    Ejemplo de uso:
    Para transferir un aparcamiento, se debe enviar una solicitud PUT a '/transfer/{parking_id}', donde '{parking_id}' es el ID del aparcamiento a transferir.
    """
    try:
        parking = Parking.objects.get(pk=parking_id, is_assignment=True, parking_type=ParkingType.ASSIGNMENT, is_transfer=False, notified_by=request.user)
        parking.is_transfer = True
        parking.save()
        return JsonResponse({"message": "Parking assigned"}, status=200)
    except Parking.DoesNotExist:
        return JsonResponse({"message": "The parking doesn't exist"}, status=404)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_parking(request: HttpRequest, parking_id: int):
    """
    Elimina un aparcamiento.

    Esta función permite a un usuario eliminar un aparcamiento que ha creado. Espera una solicitud DELETE con el ID del aparcamiento a eliminar.

    Parámetros:
    - request (HttpRequest): La solicitud HTTP.
    - parking_id (int): El ID del aparcamiento a eliminar.

    Retorna:
    - JsonResponse: En caso de éxito, retorna un JsonResponse con un mensaje de confirmación. Si el aparcamiento no existe o no fue creado por el usuario que hace la solicitud, retorna un mensaje de error.

    Ejemplo de uso:
    Para eliminar un aparcamiento, se debe enviar una solicitud DELETE a '/delete/{parking_id}', donde '{parking_id}' es el ID del aparcamiento a eliminar.
    """
    try:
        parking = Parking.objects.get(pk=parking_id, is_assignment=False)
        manage_send_parking_created(NoticationsSocket.PARKING_DELETED.value, ParkingSerializer(parking).data, parking.location)
        parking.delete()
        return JsonResponse({"message": "Parking deleted"}, status=200)
    except Parking.DoesNotExist:
        return JsonResponse({"message": "The parking doesn't exist"}, status=404)
    

@api_view(['GET'])
def create_parking_data(request: HttpRequest):
    """
    Crea un objeto que contiene los datos de la creación de aparcamientos.

    Esta función se utiliza para crear un objeto que contiene los datos de los aparcamientos.

    Parámetros:
    - request (HttpRequest): La solicitud HTTP.

    Retorna:
    - JsonResponse: Un JsonResponse con los datos de los aparcamientos.

    Ejemplo de uso:
    Para obtener"""
    res = JsonResponse({
        "parking_types": [(i.name, i.value) for i in ParkingType],
        "parking_sizes": [(i.name, i.value )for i in Size],
    })
    return res

  @api_view(['POST'])
#@login_required
def get_closest_cities(request: HttpRequest):
    """
    Obtiene las ciudades más cercanas a unas coordenadas dadas.

    Parámetros:
    - request (HttpRequest): La solicitud HTTP. Debe contener los parámetros 'latitude' y 'longitude' que representan las coordenadas desde donde buscar ciudades cercanas.

    Retorna:
    - Response: Una respuesta HTTP con un código de estado 200 y un JSON que contiene las ciudades más cercanas, o un mensaje de error si se produce algún fallo.
    """
    try:
        # Obtener las coordenadas desde la solicitud
        latitude = float(request.query_params.get('latitude'))
        longitude = float(request.query_params.get('longitude'))
        
        # Crear un punto a partir de las coordenadas dadas
        given_point = Point(longitude, latitude, srid=4326)
        
        # Obtener las ciudades ordenadas por distancia a las coordenadas dadas
        closest_cities = City.objects.annotate(distance=Distance('location', given_point)).order_by('distance')
        
        # Serializar los datos de las ciudades
        data = [{'name': city.name, 'distance': city.distance.km} for city in closest_cities]
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

