from rest_framework import serializers
from core.models import Address, Store, Category, Product


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


class StoreSerializer(serializers.ModelSerializer):
    """ Store Serializers"""

    address = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Address.objects.all()
    )

    class Meta:
        model = Store
        fields = ("id", "name", "address")
        read_only_fields = ("id",)


class CategorySerializer(serializers.ModelSerializer):

    """Category serializers"""

    class Meta:
        model = Category
        fields = ("id", "name")

        read_only_fields = ("id",)


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer"""

    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "store", "category")
        read_only_fields = ("id",)
