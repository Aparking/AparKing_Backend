from django.shortcuts import render

import stripe
import json
from django.conf import settings
from django.http import JsonResponse
from .models import MemberShip, CustomUser, Credit
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from apps.payment.enums import MemberId
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        customUser = request.user
        credit =Credit.filter(user=customUser.id)
        subscription_plan_id=MemberId.FREE
        if data.get('planId')== 'NOBLE':
            credit.value = 300
            subscription_plan_id=MemberId.NOBLE
        elif data.get('planId')== 'KING':
            credit.value = 1000
            subscription_plan_id=MemberId.KING
          
        
        memberShip =MemberShip.objects.filter(user=customUser)
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': subscription_plan_id,  # ID del precio asociado al plan(es el stripe_subcription_id del membership)
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://localhost:8100/aparking/map',
            cancel_url='http://localhost:8100/test-subscription',
        )
        print("prueba5")
        if(checkout_session.success_url == "http://localhost:8100/aparking/map"):
            customUser.stripe_subscription_id = subscription_plan_id
            memberShip.type = data.get('planId')
            credit.save()
            memberShip.save()
            customUser.save()



        return JsonResponse({'url': checkout_session.url})
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=403)
