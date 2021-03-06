from rest_framework import serializers
from core.models import Address, Store, Category, Product, Order, Invoice, Transaction

from user.serializers import UserSerializer


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
            "user",
        )
        read_only_fields = ("id", "user")


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


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for orders """

    class Meta:
        model = Order
        fields = ("id", "product", "quantity", "estimated_price")
        read_only_fields = ("id",)


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice"""

    class Meta:
        model = Invoice
        fields = (
            "id",
            "product",
            "quantity",
            "price",
            "status",
            "date_issued",
        )
        read_only_fields = ("id",)


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction"""

    invoice = InvoiceSerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "invoice",
        )

        read_only_fields = ("id",)
