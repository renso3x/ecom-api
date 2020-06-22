from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test create a new user with an email is successfull"""
        email = "test@refluens.com"
        password = 'ab123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for new user is normalize"""
        email = 'romeo@REFLUENS.COM'
        user = get_user_model().objects.create_user(email, 'testpass')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'qwerqwer')

    def test_create_new_superuser(self):
        """ Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'admin@admin.com',
            '123123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
