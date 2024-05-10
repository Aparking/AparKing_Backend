from django.test import TestCase
from apps.garagement.models import Address
from apps.garagement.serializers import AddressSerializer
from django_countries.fields import Country

class AddressSerializerTest(TestCase):
    def test_valid_serializer(self):
        valid_serializer_data = {
            "street_number": "123",
            "address_line": "Calle Falsa",
            "city": "Springfield",
            "region": "Region Test",
            "country": "US",
            "postal_code": "12345"
        }
        serializer = AddressSerializer(data=valid_serializer_data)
        self.assertTrue(serializer.is_valid())
        address = serializer.save()
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(str(address), "123, Calle Falsa, Springfield, Region Test, United States of America")
