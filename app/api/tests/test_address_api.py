from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Address

from api.serializers import AddressSerializer

ADDRESS_URL = reverse("api:address-list")


def sample_address(user):
    return Address.objects.create(
        user=user,
        address="Block 1, Lot 1, Phase 1, Ashton Fields South",
        city="Calamba City",
        latitude=14.204780,
        longitude=121.154716,
    )


def detail_url(address_id):
    """Return recipe detail URL"""
    return reverse("api:address-detail", args=[address_id])


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

    def test_retrieve_address_details(self):
        """Test viewing a address detail"""
        address = Address.objects.create(
            user=self.user,
            address="Block 1, Lot 1, Phase 1, Ashton Fields South",
            city="Calamba City",
            latitude=14.204780,
            longitude=121.154716,
        )
        # get the address id
        url = detail_url(address.id)

        res = self.client.get(url)

        serializer = AddressSerializer(address)

        self.assertEqual(res.data, serializer.data)

    def test_put_update_address(self):
        """Test updating a address with put"""
        address = sample_address(user=self.user)
        payload = {
            "address": "Walter Makiling",
            "city": "Makiling City",
            "latitude": 14.204780,
            "longitude": 121.154716,
        }

        url = detail_url(address.id)
        self.client.put(url, payload)

        address.refresh_from_db()
        self.assertEqual(address.address, payload["address"])
        self.assertEqual(address.city, payload["city"])
        self.assertEqual(str(address.latitude), "{0:.6f}".format(payload["latitude"]))
        self.assertEqual(str(address.longitude), "{0:.6f}".format(payload["longitude"]))

    def test_delete_address(self):
        """Test delete an address """
        address = sample_address(user=self.user)
        url = detail_url(address.id)
        self.client.delete(url)

        self.assertEqual(Address.objects.count(), 0)
