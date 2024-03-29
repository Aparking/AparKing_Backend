from django.shortcuts import render

import stripe
import json
from django.conf import settings
from django.http import JsonResponse
from .models import MemberShip, CustomUser
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime


stripe.api_key = settings.STRIPE_SECRET_KEY
'''
@csrf_exempt
@require_POST
def create_subscription(request):
    try:
        #to do: condicional si el usuario no tiene cuenta de stripe
       # data = json.loads(request.body.decode('utf-8'))
        #subscription_plan_id = data.get('id')
        #custom_user = request.user
        #member_ship = MemberShip.objects.filter(user=custom_user.id)
        subscription_plan_id = "price_1OzS3cC4xI44aLdHM2cgCYW4"
        custom_user = CustomUser.objects.create(
            username='alejandro',
            email='alejandro16032002@gmail.com',
            dni="49190242G",
            first_name="alejandro",
            last_name="Perez",
            gender="M",
            is_active=False,
            is_staff=False,
            date_joined=parse_datetime("2023-01-01T16:46:52.327Z"),
            birth_date="2024-02-27",
            phone="+1612348729",
            stripe_customer_id=None,
            code="valor"
        )
        #member_ship = MemberShip.objects.filter(user=custom_user.id)

        member_ship = MemberShip.objects.create(
            start_date=parse_datetime("2024-01-01T00:00:00Z"),
            end_date=parse_datetime("2024-12-31T23:59:59Z"),
            type="Gratuita",
            user=custom_user,  # Asociamos directamente el objeto user creado anteriormente
            stripe_subscription_id=None
        )
    
        customer = stripe.Customer.create(
            email = custom_user.email
        )

        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': subscription_plan_id}],
        )


        custom_user.stripe_customer_id = customer.id
        member_ship.stripe_subscription_id = subscription.id

        custom_user.save()
        member_ship.save()
        
        return JsonResponse({'status': 'success', 'subscription_id': subscription.id})
    except stripe.error.StripeError as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

'''

@csrf_exempt
@require_POST
def create_checkout_session(request):
    #a traves del request debe venirnos el valor de la subscripcion que quiere
    data = json.loads(request.body.decode('utf-8'))
    print("==============================")
    print(data)
    try:
        subscription_plan_id = "price_1OzduBC4xI44aLdHVfhBk4MT"#(pillarlo del data id a traves de un filter del membership)
        print("prueba1")
        #custom_user = CustomUser.objects.create(
        #username='alejandro',
        #email='alejandro16032002@gmail.com',
        #dni="49190242G",
        #first_name="alejandro",
        #last_name="Perez",
        #gender="M",
        #is_active=False,
        #is_staff=False,
        #date_joined=parse_datetime("2023-01-01T16:46:52.327Z"),
        #birth_date="2024-02-27",
        #phone="+1612348729",
        #stripe_customer_id=None,
        #code="valor"
   # )
    #member_ship = MemberShip.objects.filter(user=custom_user.id)
    #    print("prueba2")
     #   member_ship = MemberShip.objects.create(
      #  start_date=parse_datetime("2024-01-01T00:00:00Z"),
       # end_date=parse_datetime("2024-12-31T23:59:59Z"),
        #type="Gratuita",
        #user=custom_user,  # Asociamos directamente el objeto user creado anteriormente
        #stripe_subscription_id=None
    #)
        print("prueba3")
    #data = json.loads(request.body)
    #plan_id = data['planId']
        # Crea la sesión de Checkout con el plan seleccionado
       # customer = stripe.Customer.create(
        #    email = custom_user.email,
         #   name = custom_user.username
        #)
        print("prueba4")
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': subscription_plan_id,  # ID del precio asociado al plan(es el stripe_subcription_id del membership)
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://localhost:8100',
            cancel_url='http://localhost:8100',
        )
        print("prueba5")
        #if(checkout_session.success_url == "http://localhost:8100"):
            #custom_user.stripe_customer_id = customer.id
           # member_ship.stripe_subscription_id = subscription_plan_id

            #custom_user.save()
            #member_ship.save()



        return JsonResponse({'url': checkout_session.url})
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=403)
'''
def create_checkout_session(request):
    try:
        # Configura la clave secreta de Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Crea una sesión de checkout de Stripe para la membresía
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': "prod_Pp36TNvrf8GZlz",  # Reemplaza con el ID del precio de tu producto de membresía
                'quantity': 1,
            }],
            mode='subscription',
            success_url='',  # La URL a la que Stripe redirige después de un pago exitoso
            cancel_url='/register',   # La URL a la que Stripe redirige después de un pago cancelado
        )

        # Devuelve el ID de la sesión de checkout al frontend
        return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as e:
        return JsonResponse({'error': str(e)})
        '''