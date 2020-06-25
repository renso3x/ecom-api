from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Store, Address

from api.serializers import StoreSerializer

STORE_URL = reverse("api:store-list")


def sample_address(user):
    return Address.objects.create(
        user=user,
        address="Block 1, Lot 1, Phase 1, Ashton Fields South",
        city="Calamba City",
        latitude=14.204780,
        longitude=121.154716,
    )


def sample_store(user, **params):
    defaults = {
        "name": "Pasabuy SNR and Landers",
    }
    defaults.update(params)

    return Store.objects.create(user=user, **defaults)


def detail_url(store_id):
    """Return recipe detail URL"""
    return reverse("api:store-detail", args=[store_id])


class PublicAddressApiTest(TestCase):
    """Test the public available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(STORE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAddressApiTest(TestCase):
    """Test Address  can be retrieve by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@refluens.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_store_list(self):
        """Test on all store"""
        sample_store(user=self.user)
        sample_store(user=self.user)

        res = self.client.get(STORE_URL)
        stores = Store.objects.all().order_by("-id")
        serializer = StoreSerializer(stores, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_store_success(self):
        """Test create store success"""
        address1 = sample_address(user=self.user)
        payload = {"name": "BuyKita store", "address": [address1.id]}

        res = self.client.post(STORE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        store = Store.objects.get(id=res.data["id"])
        address = store.address.all()

        self.assertEqual(address.count(), 1)
        self.assertIn(address1, address)

    def test_update_store_success(self):
        """Test updating a recipe with patch"""
        store = sample_store(user=self.user)
        store.address.add(sample_address(user=self.user))

        payload = {
            "name": "PasaBuy",
        }

        url = detail_url(store.id)
        self.client.patch(url, payload)

        store.refresh_from_db()

        self.assertEqual(store.name, payload["name"])

    def test_delete_store_success(self):
        """Test delete a store"""
        store = sample_store(user=self.user)
        url = detail_url(store.id)
        self.client.delete(url)

        self.assertEqual(Store.objects.count(), 0)
