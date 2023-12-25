from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomModelBackend(ModelBackend):
    """Log in to Django without providing a password.
    """
    def authenticate(self, request, username):
        print('backe'*10)
        User = get_user_model()
        try:
            user = User.objects.get(phone_number=username)
            return user
        except User.DoesNotExist:
            return None

        