from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Address, Store, Category, Product
from api import serializers


class BaseApiAttrViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """Base viewset for user owned recipe attrs"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """create a new object"""
        return serializer.save(user=self.request.user)


class AddressViewSet(BaseApiAttrViewSet):
    """Manage address in the database """

    queryset = Address.objects.all()
    serializer_class = serializers.AddressSerializer


class StoreViewSet(BaseApiAttrViewSet):
    """ Manage store in the database"""

    queryset = Store.objects.all()
    serializer_class = serializers.StoreSerializer


class CategoryViewSet(BaseApiAttrViewSet):
    """Manage category in the database"""

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return self.queryset.filter()

    def perform_create(self, serializer):
        """create a new object"""
        return serializer.save()


class ProductViewSet(BaseApiAttrViewSet):
    """ Manage Product in the database """

    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the recipes for the auth user"""
        categories = self.request.query_params.get("categories")
        queryset = self.queryset

        if categories:
            cat_ids = self._params_to_ints(categories)
            queryset = queryset.filter(category__id__in=cat_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "retrieve":
            return serializers.ProductDetailSerializer
        elif self.action == "upload_image":
            return serializers.ProductImageSerializer

        return self.serializer_class

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to a product"""
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
