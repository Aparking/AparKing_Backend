import re
from apps.authentication.models import CustomUser,Vehicle
from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if user:
            return user
        raise serializers.ValidationError("Credenciales incorrectas")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "dni", "phone", "birth_date")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            dni=validated_data["dni"],
            phone=validated_data["phone"],
            birth_date=validated_data["birth_date"],
        )
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "dni", "birth_date", "gender", "phone", "username")

class RegisterVehicleSerializer(serializers.ModelSerializer):
    SPANISH_COLORS = [
        "rojo", "verde", "azul", "amarillo", "naranja", 
        "violeta", "rosa", "blanco", "negro", "gris"
    ]
    class Meta:
        model = Vehicle
        fields = ("carModel", "color", "height", "width", "length","owner")

    def validate_color(self, value):
        if value.lower() not in self.SPANISH_COLORS:
            raise serializers.ValidationError("El color ingresado no es válido.")
        return value
    
    def validate_height(self, value):
        if value < 0:
            raise serializers.ValidationError("La altura no puede ser negativa.")
        return value

    def validate_width(self, value):
        if value < 0:
            raise serializers.ValidationError("La anchura no puede ser negativa.")
        return value

    def validate_length(self, value):
        if value < 0:
            raise serializers.ValidationError("La longitud no puede ser negativa.")
        return value
    
    def create(self, validated_data):
        vehicle = Vehicle.objects.create(
            carModel=validated_data["carModel"],
            color=validated_data["color"],
            height=validated_data["height"],
            width=validated_data["width"],
            length=validated_data["length"],
            owner=validated_data["owner"],
        )
        return vehicle
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("birth_date","dni","email", "phone", "username")