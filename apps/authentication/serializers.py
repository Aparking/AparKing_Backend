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
    class Meta:
        model = Vehicle
        fields = ("carModel", "color", "height", "width", "length","owner")

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