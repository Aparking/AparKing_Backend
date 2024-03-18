from apps.garagement.models import Address, Availability, Garage, Image
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Image
        fields = ["image", "alt"]


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = "__all__"


class GarageSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    image = ImageSerializer(many=False, required=False)

    class Meta:
        model = Garage
        fields = [
            "name",
            "description",
            "height",
            "width",
            "length",
            "price",
            "creation_date",
            "modification_date",
            "is_active",
            "owner",
            "address",
            "image",
        ]

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        image_data = validated_data.pop("image")

        address = Address.objects.create(**address_data)
        garage = Garage.objects.create(address=address, **validated_data)

        Image.objects.create(garage=garage, **image_data)
        return garage

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address")
        images_data = validated_data.pop("images")

        instance = super().update(instance, validated_data)

        if address_data:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()

        for image_data in images_data:
            image_id = image_data.get("id", None)
            if image_id:
                image = Image.objects.get(pk=image_id, garage=instance)
                for attr, value in image_data.items():
                    setattr(image, attr, value)
                image.save()
            else:
                Image.objects.create(garage=instance, **image_data)

        return instance
