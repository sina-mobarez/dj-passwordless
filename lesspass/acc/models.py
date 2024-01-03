from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator

from .base_user import AbstractBaseUser, CustomUserManager
import pyotp


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with phone number authentication and OTP support.
    """

    phone_regex = RegexValidator(
        regex=r'^9\d{9}$',
        message='Phone number must be entered in the format 9xxxxxxxxx. Up to 10 digits allowed.'
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    key = models.CharField(max_length=100, unique=True, blank=True)

    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()

    def authenticate_otp_code(self, otp):
        """
        Authenticate the given OTP.

        Args:
            otp (str): The OTP code to be authenticated.

        Returns:
            bool: True if the OTP is valid, False otherwise.
        """
        provided_otp = 0
        try:
            provided_otp = int(otp)
        except ValueError:
            return False

        # Using Time Based OTP with a 180 seconds interval
        t = pyotp.TOTP(self.key, interval=180)
        return t.verify(provided_otp)

    def __str__(self) -> str:
        """
        String representation of the user object.

        Returns:
            str: The phone number of the user.
        """
        return self.phone_number
