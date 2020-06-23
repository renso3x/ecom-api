from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Address

from api.serializers import AddressSerializer

ADDRESS_URL = reverse("api:address-list")


class PublicAddressApiTest(TestCase):
    """Test the public available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(ADDRESS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAddressApiTest(TestCase):
    """Test Address  can be retrieve by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@refluens.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_address_list(self):
        """ Test address list of authenticated user"""
        Address.objects.create(
            user=self.user,
            address="Block 1, Lot 1, Phase 1, Ashton Fields South",
            city="Calamba City",
            latitude=14.204780,
            longitude=121.154716,
        )

        res = self.client.get(ADDRESS_URL)
        addressess = Address.objects.all()
        serializer = AddressSerializer(addressess, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_address_success(self):
        """Test create address return success"""
        payload = {
            "user": self.user,
            "address": "Block 2, Lot 13, Phase 3, Ashton Fields South",
            "city": "Calamba City",
            "latitude": 14.204780,
            "longitude": 121.154716,
        }
        self.client.post(ADDRESS_URL, payload)

        exists = Address.objects.filter(
            user=self.user, address=payload["address"]
        ).exists()

        self.assertTrue(exists)

    def test_create_address_invalid(self):
        """ Test create address return invalid"""
        payload = {
            "address": "",
        }

        res = self.client.post(ADDRESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

