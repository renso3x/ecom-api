from rest_framework import serializers
from core.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """Address serializers"""

    class Meta:
        model = Address
        fields = (
            "id",
            "address",
            "city",
            "latitude",
            "longitude",
        )
        read_only_fields = ("id",)

