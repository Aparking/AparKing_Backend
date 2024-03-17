from rest_framework import serializers

from . import validations
from .enums import ClaimStatus
from .models import Claim

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['title', 'description', 'status', 'user', 'garage']

    def validate(self, attrs):
        return validations.validate_claim_data(attrs, ClaimStatus)