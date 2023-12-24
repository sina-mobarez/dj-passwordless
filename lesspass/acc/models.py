from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.apps import apps
from .base_user import AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, email, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            raise ValueError("The given phone must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, email, **extra_fields)

    def create_superuser(self, phone_number, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique= True, null=False)
    phone_regex = RegexValidator(regex='^(\+98|0)?9\d{9}$', message='Phone number must be entered in the format 9xxxxxxxxx. Up to 10 digits allowed.')
    phone_number = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = ['email',]

    objects = CustomUserManager()
    

    def __str__(self) -> str:
        return self.phone_number


class Profile(models.Model):
    name = models.CharField(max_length=50, null= True)
    age = models.DateField(null=True)
    bio = models.TextField(null=True)
    image = models.ImageField(null=True)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name