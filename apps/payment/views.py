from django.shortcuts import render

import stripe
from django.conf import settings
from django.http import JsonResponse
from .models import MemberShip, CustomUser

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_subscription(request):
    # Asumiendo que recibes el ID del plan de suscripción y el token de Stripe desde el frontend
    subscription_plan_id = 'plan_id'
    token = 'stripe_token'
    custom_user = request.user
    member_ship = MemberShip.objects.filter(user=custom_user.id)

    try:
        customer = stripe.Customer.create(
            email = custom_user.email
            source = token  # Obtenido desde el frontend
        )

        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'plan': subscription_plan_id}],
        )
        custom_user.stripe_customer_id = customer.id
        member_ship.stripe_subscription_id = subscription.id

        custom_user.save()
        member_ship.save()
        
        # Aquí puedes guardar la suscripción en tu base de datos, si es necesario
        return JsonResponse({'status': 'success', 'subscription_id': subscription.id})
    except stripe.error.StripeError as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
