from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Address
from api import serializers


class BaseApiAttrViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
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

