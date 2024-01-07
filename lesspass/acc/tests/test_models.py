from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
import pyotp

class CustomUserModelTest(TestCase):

    def setUp(self):
        # Create a CustomUser instance for testing
        self.user = get_user_model().objects.create(phone_number='9123456789')
        # Create an OTP code
        self.valid_otp = str(pyotp.TOTP(self.user.key, interval=180).now())  

    def test_create_user(self):
        """Test creating a new CustomUser instance."""
        self.assertIsInstance(self.user, get_user_model())
        self.assertEqual(self.user.phone_number, '9123456789')
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_active)

    def test_str_method(self):
        """Test the string representation of the user."""
        self.assertEqual(str(self.user), '9123456789')

    def test_authenticate_otp_code_valid(self):
        """Test authenticating a valid OTP code."""
        self.assertTrue(self.user.authenticate_otp_code(self.valid_otp))

    def test_authenticate_otp_code_invalid(self):
        """Test authenticating an invalid OTP code."""
        invalid_otp = '987654'  # Use an invalid OTP code for testing
        self.assertFalse(self.user.authenticate_otp_code(invalid_otp))

    def test_duplicate_phone_number_not_allowed(self):
        """Test that creating a user with a duplicate phone number raises an error."""
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create(phone_number='9123456789', key='another_key')

    def test_create_user(self):
        user = get_user_model().objects.create_user(phone_number='9999999999')
        self.assertEqual(user.phone_number, '9999999999')

    def test_create_superuser(self):
        admin_user = get_user_model().objects.create_superuser(phone_number='9999999999'
        )
        self.assertEqual(admin_user.phone_number, '9999999999')
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)