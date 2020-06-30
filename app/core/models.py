from django.utils.translation import gettext_lazy as _
import uuid
import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


def product_image_file_path(instance, filename):
    """Generate file path for new product image"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("uploads/products", filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """ Create and saves a new user """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        # encrypt the password
        user.set_password(password)
        # supports multiple database
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Creates and saves a new super user """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def __str__(self):
        return self.email


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model supports email instead of username """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Address(models.Model):
    """Address attributes"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.address


class Store(models.Model):
    """ Store attributes"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.ManyToManyField("Address")

    def __str__(self):
        return self.name


class Category(models.Model):
    """ Category attributes"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Product attributes"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    category = models.ManyToManyField("Category")
    store = models.ForeignKey("Store", on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, upload_to=product_image_file_path)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Order attributes"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    estimated_price = models.DecimalField(max_digits=6, decimal_places=2)


class Invoice(models.Model):
    """Invoice attributes"""

    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Status(models.TextChoices):
        ISSUED = (
            "ISSUED",
            "Issued",
        )
        PICKED_UP = (
            "PICKED_UP",
            "Pick-Up",
        )
        COMPLETED = (
            "COMPLETED",
            "Completed",
        )
        CANCELLED = "CANCELLED", "Cancelled"

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ISSUED
    )
    date_issued = models.DateTimeField(
        _(""), auto_now=False, auto_now_add=True, null=True
    )
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self


class Transaction(models.Model):
    """Transaction attributes"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE)

    def __str__(self):
        return self
