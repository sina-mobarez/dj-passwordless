from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.apps import apps
from .base_user import AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            raise ValueError("The given phone must be set")
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(phone_number=phone_number, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, **extra_fields)

    def create_superuser(self, phone_number, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^9\d{9}$', message='Phone number must be entered in the format 9xxxxxxxxx. Up to 10 digits allowed.')
    phone_number = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    key = models.CharField(max_length=100, unique=True, blank=True)

    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()
    
    
    def authenticate(self, otp):
        """ This method authenticates the given otp"""
        provided_otp = 0
        try:
            provided_otp = int(otp)
        except:
            return False
        #Here we are using Time Based OTP. The interval is 60 seconds.
        #otp must be provided within this interval or it's invalid
        t = pyotp.TOTP(self.key, interval=300)
        return t.verify(provided_otp)    
    

    def __str__(self) -> str:
        return self.phone_number
