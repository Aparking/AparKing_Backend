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

@api_view(['PUT'])
def update_claim(request, pk) -> Response:
    try:
        claim = Claim.objects.get(pk=pk)
    except Claim.DoesNotExist:
        return Response({'status': 'not found'}, status=404)

    serializer = ClaimSerializer(claim, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success'})
    else:
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_claim(request, pk) -> Response:
    try:
        claim = Claim.objects.get(pk=pk)
    except Claim.DoesNotExist:
        return Response({'status': 'not found'}, status=404)

    claim.delete()
    return Response({'status': 'success'})