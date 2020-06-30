from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product, Invoice, Product

from api.serializers import InvoiceSerializer

INVOICE_URL = reverse("api:invoice-list")


def detail_url(invoice_url):
    """Return detail URL"""
    return reverse("api:invoice-detail", args=[invoice_url])


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


class PublicInvoiceApiTest(TestCase):
    """Test the public available invoice API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INVOICE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateInvoiceApiTest(TestCase):
    """Test Invoice  can be retrieve by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@refluens.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrive_invoice_list(self):
        """ test retrieve a list of invoice"""
        Invoice.objects.create(
            user=self.user,
            product=sample_product(self.user),
            status="ISSUED",
            quantity=1,
            price=500.00,
        )
        Invoice.objects.create(
            user=self.user,
            product=sample_product(self.user),
            status="ISSUED",
            quantity=2,
            price=1500.00,
        )

        res = self.client.get(INVOICE_URL)
        invoice = Invoice.objects.filter(user=self.user)
        serializer = InvoiceSerializer(invoice, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_invoice(self):
        """Test create an invoice success"""
        product = sample_product(user=self.user, name="Desk Lamp", price=600.00)
        payload = {
            "user": sample_buyer(),
            "product": product,
            "status": "ISSUED",
            "quantity": 1,
            "price": product.price,
        }

        res = self.client.post(INVOICE_URL, payload)
        self.assertTrue(res.status_code, status.HTTP_201_CREATED)

    def test_create_invoice_invalid(self):
        """Test invalid invoice"""
        payload = {"user": 1, "product": sample_product(user=self.user)}

        res = self.client.post(INVOICE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_detail(self):
        """Test update invoice details"""
        product = sample_product(user=self.user, name="Desk Lamp", price=600.00)
        invoice = Invoice.objects.create(
            user=self.user,
            product=product,
            status="ISSUED",
            quantity=1,
            price=product.price,
        )
        payload = {"status": "PICKED_UP"}

        url = detail_url(invoice.id)
        self.client.patch(url, payload)

        invoice.refresh_from_db()

        self.assertEqual(invoice.status, payload["status"])

    def test_delete_invoice(self):
        """ Test delete an invoice created"""
        invoice = Invoice.objects.create(
            user=self.user,
            product=sample_product(self.user),
            status="ISSUED",
            quantity=2,
            price=1500.00,
        )

        url = detail_url(invoice.id)

        self.client.delete(url)

        self.assertEqual(Invoice.objects.count(), 0)

    def test_filter_invoice_by_status(self):
        """ Test Invoice retrieve on what status"""
        inv1 = Invoice.objects.create(
            user=self.user,
            product=sample_product(self.user),
            status="ISSUED",
            quantity=2,
            price=1500.00,
        )
        inv2 = Invoice.objects.create(
            user=self.user,
            product=sample_product(self.user),
            status="ISSUED",
            quantity=2,
            price=1500.00,
        )
        inv3 = Invoice.objects.create(
            user=self.user,
            product=sample_product(self.user),
            status="PICK_UP",
            quantity=2,
            price=1500.00,
        )

        res = self.client.get(INVOICE_URL, {"status": f"{inv1.status}"})

        s1 = InvoiceSerializer(inv1)
        s2 = InvoiceSerializer(inv2)
        s3 = InvoiceSerializer(inv3)

        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)

    def test_invoice_transaction_create(self):
        """Test create transaction if invoice is completed"""

