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

    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "store",
            "category",
            "image",
        )
        read_only_fields = ("id",)


class ProductDetailSerializer(ProductSerializer):
    """ Serializer for product detail"""

    category = CategorySerializer(many=True, read_only=True)


class ProductImageSerializer(ProductSerializer):
    """Serializers for uploading images to product"""

    class Meta:
        model = Product
        fields = (
            "id",
            "image",
        )
        read_only_fields = ("id",)
