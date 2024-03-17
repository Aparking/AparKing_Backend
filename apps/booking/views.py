from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Claim
from .serializers import ClaimSerializer

@api_view(['POST'])
def create_claim(request) -> Response:
    serializer = ClaimSerializer(data=request.data)
    if serializer.is_valid():
        claim = serializer.save()
        return Response({'status': 'success', 'claim_id': claim.id})
    else:
        return Response(serializer.errors, status=400)

