from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Address, Store, Category
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
