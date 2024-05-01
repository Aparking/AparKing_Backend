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
from apps.payment.enums import MemberId, MemberType
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from dateutil.relativedelta import relativedelta
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        customUser = request.user
        credit =Credit.objects.get(user=customUser.id)
        memberShip =MemberShip.objects.filter(user=customUser).latest('start_date')
        subscription_plan_id=MemberId.FREE
        if data.get('planId')== 'NOBLE':
            credit.value = 300
            subscription_plan_id=MemberId.NOBLE
        elif data.get('planId')== 'KING':
            credit.value = 1000
            subscription_plan_id=MemberId.KING
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': subscription_plan_id,  # ID del precio asociado al plan(es el stripe_subcription_id del membership)
                'quantity': 1,
            }],
            mode='subscription',
            success_url=data['url'],
            cancel_url=data['url'],
        )
        userInfo={
            'name':customUser.username,
            'membership':memberShip.type,
            'credit': credit.value
        }

        response_data={
            'url': checkout_session.url,
            'user_info':userInfo
        }
        customUser.stripe_session_id = checkout_session.id
        customUser.save()

        return JsonResponse(response_data)
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=403)
    
@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMembership(request):
    try:
        customUser = request.user
        credit =Credit.objects.get(user=customUser.id)
        memberShip =MemberShip.objects.get(user=customUser)
        subscription_plan_id=MemberId.FREE
        member=MemberType.FREE
        if(customUser.stripe_session_id!= None):
            session = stripe.checkout.Session.retrieve(customUser.stripe_session_id,expand=['line_items'])
            for item in session.line_items.data:
                if (item.price.id == str(MemberId.NOBLE)):
                    credit.value = 300
                    subscription_plan_id=MemberType.NOBLE
                    member=MemberType.NOBLE
                elif (item.price.id ==str(MemberId.KING)):
                    credit.value = 1000
                    subscription_plan_id=MemberId.KING
                    member=MemberType.KING
                if(session.payment_status != "unpaid" and customUser.stripe_subscription_id != None):
                    customUser.stripe_subscription_id = subscription_plan_id
                    now = timezone.now()
                    oneMonthLater = now + relativedelta(months=1)
                    formattedNow = now.strftime('%Y-%m-%d %H:%M')
                    formattedOneMonthLater = oneMonthLater.strftime('%Y-%m-%d %H:%M')
                    memberShip.start_date=formattedNow
                    memberShip.end_date=formattedOneMonthLater
                    memberShip.type = member
                    memberShip.stripe_subscription_id=customUser.stripe_subscription_id
                    customUser.stripe_subscription_id=None
                    credit.save()
                    memberShip.save()
                    customUser.save()
        userInfo={
            'user':customUser.to_json(),
            'membership':memberShip.to_json(),
            'credit': credit.to_json()
        }
        response_data={
            'user_info':userInfo
        }
        return JsonResponse(response_data)
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=403)
