from django.utils import timezone
from rest_framework import serializers

def validate_title(title):
    if not title or not isinstance(title, str) or len(title) > 64:
        raise serializers.ValidationError("El título debe ser una cadena no vacía de máximo 64 caracteres.")

def validate_description(description):
    if not description or not isinstance(description, str) or len(description) > 1024:
        raise serializers.ValidationError("La descripción debe ser una cadena no vacía de máximo 1024 caracteres.")

def validate_claim_data(claim_data, ClaimStatus):
    title = claim_data.get('title', None)
    validate_title(title)
    
    description = claim_data.get('description', None)
    validate_description(description)
    
    return claim_data
