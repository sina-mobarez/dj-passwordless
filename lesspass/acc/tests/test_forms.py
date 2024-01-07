from django.test import TestCase
from django.contrib.auth import get_user_model
import pyotp
from ..forms import CustomAuthenticationForm

class TestCustomAuthenticationForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone_number='9123456789',
            is_active=True
        )
        self.valid_otp = str(pyotp.TOTP(self.user.key, interval=180).now())

    def test_valid_credentials(self):
        data = {'username': '9123456789', 'otp_code': self.valid_otp}
        form = CustomAuthenticationForm(data=data, request=self.client)
        self.assertTrue(form.is_valid())

    def test_invalid_username(self):
        data = {'username': 'invalid_username', 'otp_code': self.valid_otp}
        form = CustomAuthenticationForm(data=data, request=self.client)
        self.assertFalse(form.is_valid())
        self.assertIn('phone number', form.errors['__all__'][0])

    def test_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        data = {'username': '9123456789', 'otp_code': self.valid_otp}
        form = CustomAuthenticationForm(data=data, request=self.client)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('inactive', form.errors['__all__'][0])

    def test_get_user(self):
        data = {'username': '9123456789', 'otp_code': self.valid_otp}
        form = CustomAuthenticationForm(data=data, request=self.client)
        form.is_valid()
        user = form.get_user()
        self.assertEqual(user, self.user)

    def test_get_invalid_login_error(self):
        data = {'username': '9123456789', 'otp_code': 'invalid_otp'}
        form = CustomAuthenticationForm(data=data, request=self.client)
        form.is_valid()
        error = form.get_invalid_login_error()
        self.assertIn('invalid_login', error.code)
        self.assertIn('phone number', error.params['username'].lower())  # Assuming USERNAME_FIELD is 'phone_number'
