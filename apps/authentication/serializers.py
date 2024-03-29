from apps.authentication.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            return user
        raise serializers.ValidationError("Credenciales incorrectas")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'dni', 'phone', 'birth_date')
        extra_kwargs = {'password': {'write_only': True}, 'username': {'validators': []}}

    def validate_username(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("El nombre de usuario debe tener datos.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            dni=validated_data['dni'],
            phone=validated_data['phone'],
            birth_date=validated_data['birth_date']
        )
        return user