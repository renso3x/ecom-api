from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product, Store, Category

from api.serializers import ProductSerializer

PRODUCT_URL = reverse("api:product-list")


def sample_category(name="Toys"):
    return Category.objects.create(name=name)


def sample_store(user, name="Toy Kingdom MOA"):
    return Store.objects.create(user=user, name=name)


def sample_product(user):
    defaults = {
        "name": "Iron Man FunKo",
        "description": "A funko pop",
        "price": 200.00,
    }

    return Product.objects.create(user=user, **defaults)


def detail_url(product_id):
    """Return detail URL"""
    return reverse("api:product-detail", args=[product_id])


class PublicProductApiTest(TestCase):
    """ Test the public api """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test the login is required to access the endpoint """

        res = self.client.post(PRODUCT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductApiTest(TestCase):
    """Test Product can be retrieve by authorized users"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@refluens.com", "testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_product_list(self):
        """ Test retrieve all products """

        sample_product(user=self.user)
        sample_product(user=self.user)

        res = self.client.get(PRODUCT_URL)
        products = Product.objects.all().order_by("-id")
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_product_invalid(self):
        """Test create a product INVALID"""
        payload = {
            "user": self.user,
            "name": "One Piece Figure",
            "description": "Complete set of 1 piece",
            "price": 600.00,
        }

        res = self.client.post(PRODUCT_URL, payload)

        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_success(self):
        """Test create a product SUCCESS"""
        cat = sample_category()
        payload = {
            "user": self.user,
            "name": "Franky Pop",
            "description": "Toy",
            "price": 5.00,
            "category": [cat.id],
        }

        self.client.post(PRODUCT_URL, payload)

        exists = Product.objects.filter(user=self.user, name=payload["name"]).exists()

        self.assertTrue(exists)

    def test_product_view(self):
        """Test Product detail view """
        p1 = sample_product(user=self.user)

        url = detail_url(p1.id)

        res = self.client.get(url)
        serializer = ProductSerializer(p1)

        self.assertEqual(res.data, serializer.data)

    def test_patch_update_product(self):
        """Test product update details"""
        product = sample_product(user=self.user)
        payload = {"name": "Gundam: Exia", "description": "Gunpla", "price": 1500.00}

        url = detail_url(product.id)

        self.client.patch(url, payload)

        product.refresh_from_db()
        self.assertEqual(product.name, payload["name"])
        self.assertEqual(product.description, payload["description"])
        self.assertEqual(product.price, payload["price"])

    def test_delete_product(self):
        """Test product delete"""
        product = sample_product(user=self.user)
        url = detail_url(product.id)
        self.client.delete(url)

        self.assertEqual(Product.objects.count(), 0)

