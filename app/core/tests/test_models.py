from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@refluens.com", password="testpass"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test create a new user with an email is successfull"""
        email = "test@refluens.com"
        password = "ab123"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for new user is normalize"""
        email = "romeo@REFLUENS.COM"
        user = get_user_model().objects.create_user(email, "testpass")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "qwerqwer")

    def test_create_new_superuser(self):
        """ Test creating a new superuser"""
        user = get_user_model().objects.create_superuser("admin@admin.com", "123123")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_address_str(self):
        """Test address string representaion"""
        my_address = models.Address.objects.create(
            user=sample_user(),
            address="Block 2, Lot 13, Phase 3, Ashton Fields South",
            city="Calamba City",
            latitude=14.204780,
            longitude=121.154716,
        )

        self.assertEqual(str(my_address), my_address.address)

    def test_product_str(self):
        """Test product string representation"""
        product = models.Product.objects.create(
            user=sample_user(),
            name="Iphone 7 Plus",
            description="Jet black variant Iphone7+",
            price=99.99,
        )
        self.assertEqual(str(product), product.name)

    def test_store_str(self):
        """Test store """
        owner = get_user_model().objects.create_user("romeo@store.com", "jinja123")
        store = models.Store.objects.create(
            user=owner, name="Pasabuy SNR and Landers"
        )

        self.assertEqual(str(store), store.name)
