from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import pyotp


def generate_key():
    """Generate a unique OTP key."""
    key = pyotp.random_base32()
    if is_unique(key):
        return key
    return generate_key()


def is_unique(key):
    """Check if the generated OTP key is unique in the database."""
    try:
        get_user_model().objects.get(key=key)
    except get_user_model().DoesNotExist:
        return True
    return False


@receiver(pre_save, sender=get_user_model())
def create_key(sender, instance, **kwargs):
    """Create an OTP key for a user before saving the instance."""
    if not instance.key:
        instance.key = generate_key()
