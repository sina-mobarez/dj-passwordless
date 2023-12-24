from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import pyotp
        
        
        
def generate_key():
    """ User otp key generator """
    key = pyotp.random_base32()
    if is_unique(key):
        return key
    generate_key()
    
    

def is_unique(key):
    try:
        get_user_model().objects.get(key=key)
    except get_user_model().DoesNotExist:
        return True
    return False
    

@receiver(pre_save, sender=get_user_model())
def create_key(sender, instance, **kwargs):

    if not instance.key:
        instance.key = generate_key()