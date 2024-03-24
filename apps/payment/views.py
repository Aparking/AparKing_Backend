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

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@require_POST
@login_required
def create_subscription(request):
    try:
        # Asumiendo que recibes el ID del plan de suscripción y el token de Stripe desde el frontend
        data = json.loads(request.body.decode('utf-8'))
        subscription_plan_id = data.get('id')
        custom_user = request.user
        member_ship = MemberShip.objects.filter(user=custom_user.id)

    
        customer = stripe.Customer.create(
            email = custom_user.email
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
