from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category

from api.serializers import CategorySerializer

CATEGORY_URL = reverse("api:category-list")


def detail_url(category_id):
    """Return recipe detail URL"""
    return reverse("api:category-detail", args=[category_id])


class CategoryApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@refluens.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_category_list(self):
        """ Test category list"""
        Category.objects.create(name="Food & Drinks")
        Category.objects.create(name="Electorincs")

        res = self.client.get(CATEGORY_URL)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_category_success(self):
        """Test create category return success"""
        payload = {
            "name": "Miscellaneous",
        }
        self.client.post(CATEGORY_URL, payload)

        exists = Category.objects.filter(name=payload["name"]).exists()

        self.assertTrue(exists)

    def test_create_category_invalid(self):
        """ Test create category return invalid"""
        payload = {
            "name": "",
        }

        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_category_details(self):
        """Test viewing a category detail"""
        cat1 = Category.objects.create(name="Food & Drinks")
        # get the category id
        url = detail_url(cat1.id)

        res = self.client.get(url)

        serializer = CategorySerializer(cat1)

        self.assertEqual(res.data, serializer.data)

    def test_put_update_category(self):
        """Test updating a category with put"""
        cat = Category.objects.create(name="Food & Drinks")
        payload = {"name": "Merchant plus"}

        url = detail_url(cat.id)
        self.client.put(url, payload)

        cat.refresh_from_db()
        self.assertEqual(cat.name, payload["name"])

    def test_delete_category(self):
        """Test delete an category """
        cat = Category.objects.create(name="Food & Drinks")
        url = detail_url(cat.id)
        self.client.delete(url)

        self.assertEqual(Category.objects.count(), 0)
