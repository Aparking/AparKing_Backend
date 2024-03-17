from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import ClaimSerializer
from .models import Claim


class ClaimAdminListAPIView(ListCreateAPIView):
    serializer_class = ClaimSerializer
    queryset = Claim.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
