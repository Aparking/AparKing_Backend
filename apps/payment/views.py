from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta
from apps.payment.models import Credit, MemberShip


@api_view(['POST'])
def pricingPlan(request) -> Response:
    data = request.data
    # Obtener datos del usuario y el plan elegido
    user_data = data.get('user', {})
    plan_type = data.get('type', None)
    price = data.get('price', 0.00)
    # Crear membresía para el usuario
    MemberShip.objects.create(
        user_id=user_data.get('id'),  # Asignar el ID del usuario
        type=plan_type,
        price=price,
        start_date=timezone.now(),  # Usar la fecha actual como fecha de inicio
        end_date=timezone.now() + relativedelta(months=+1)  # Fecha de finalización dentro de un mes
    )
    # Asignar créditos al usuario según el plan elegido
    if plan_type == 'Noble':  # Si el plan es Noble
        credits = 100  # Asignar 100 créditos
    elif plan_type == 'King':  # Si el plan es King
        credits = 200  # Asignar 200 créditos
    else:  # Si el plan es gratuito u otro tipo no especificado
        credits = 0  # No asignar créditos
    # Crear créditos para el usuario
    Credit.objects.create(
        user_id=user_data.get('id'),  # Asignar el ID del usuario
        value=credits,  # Valor del crédito
        creation_date=timezone.now()  # Usar la fecha actual como fecha de creación
    )
    return Response({'status': 'success'})
