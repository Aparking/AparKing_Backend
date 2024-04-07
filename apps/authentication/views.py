from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from .serializers import LoginSerializer, RegisterSerializer
from apps.mailer import generic_sender as Mailer
from apps.utils import code_generator
import stripe
from apps.payment.models import MemberShip, CustomUser, Credit
from apps.payment.enums import MemberType
from django.utils import timezone
from dateutil.relativedelta import relativedelta

@api_view(['POST'])
def auth_login(request) -> Response:
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        Token.objects.filter(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=200)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
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
    
@api_view(['POST'])
def verify_user(request) -> Response:
    try:
        token = Token.objects.get(key=request.data["token"])
        if token:
            user = token.user
            if user.code == request.data['code']:
                user.is_active = True
                user.save()
                token.delete()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token':token.key}, status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=400)
    except Exception:
        return Response({"error": "Token not found"}, status=400)

    
@api_view(['POST'])
def register(request) -> Response:
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False
        user.code = code_generator.code_generator(10)
        token, _ = Token.objects.get_or_create(user=user)
        Mailer.send_email(
            subject=f'AparKing - Activar cuenta',
            message=f'Bienvenido {user.first_name}, para activar su cuenta introduzca el siguiente código: {user.code}',
            mail_to=user.email
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
        return Response({'token':token.key}, status=200)
    else:
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def auth_logout(request) -> Response:
    user = request.user
    if user.is_authenticated:
        Token.objects.filter(user=user).delete()
        return Response(status=200)
    return Response(status=401)
