from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product, Order

from api.serializers import OrderSerializer

ORDER_URL = reverse("api:order-list")


def detail_url(order_id):
    """Return recipe detail URL"""
    return reverse("api:order-detail", args=[order_id])


def sample_buyer():
    return get_user_model().objects.create_user("romeo@buyer.com", "jinja123")


def sample_product(user, **params):
    defaults = {
        "name": "Iron Man FunKo",
        "description": "A funko pop",
        "price": 200.00,
    }

    defaults.update(params)

    return Product.objects.create(user=user, **defaults)


class PublicOrderApiTest(TestCase):
    """Test the public available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(ORDER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderApiTest(TestCase):
    """Test Order  can be retrieve by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@refluens.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_get_orders_list(self):
        """Get the orders from a specifc user"""
        buyer = sample_buyer()
        p1 = sample_product(user=self.user)
        Order.objects.create(
            user=buyer, product=p1, quantity=3, estimated_price=p1.price,
        )
        p2 = sample_product(user=self.user, name="Desk Lamp", price=600.00)
        Order.objects.create(
            user=buyer, product=p2, quantity=1, estimated_price=p2.price,
        )

        self.client.get(ORDER_URL)
        orders = Order.objects.all().order_by("-id")
        self.assertEqual(len(orders), 2)

    def test_create_order(self):
        """Test create an order for a customer"""
        product = sample_product(user=self.user, name="Desk Lamp", price=600.00)
        payload = {
            "user": sample_buyer(),
            "product": product,
            "quantity": 2,
            "estimated_price": product.price * 2,
        }

        res = self.client.post(ORDER_URL, payload)

        self.assertTrue(res.status_code, status.HTTP_201_CREATED)

    def test_create_order_invalid(self):
        """Test invalid order"""

        payload = {"user": sample_buyer(), "product": "Brook One Peice"}

        res = self.client.post(ORDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
