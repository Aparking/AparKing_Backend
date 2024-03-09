from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MemberShipSerializer
from .serializers import CreditSerializer

@api_view(['POST'])
def pricingPlan(request) -> Response:
    serializer = MemberShipSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        
        return Response({'status': 'success'})
    else:
        return Response(serializer.errors, status=400)
