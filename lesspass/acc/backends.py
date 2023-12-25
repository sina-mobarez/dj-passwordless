from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from multiprocessing import AuthenticationError

class CustomModelBackend(ModelBackend):
    """Log in to Django without providing a password.
    """
    def authenticate(self, request, username, otp_code):
        User = get_user_model()
        try:
            user = User.objects.get(phone_number=username)
            if otp_code:
                if user.authenticate_otp_code(otp_code):
                    return user
                else:
                    raise AuthenticationError('Your OTP code has expired.')
        except (User.DoesNotExist, AuthenticationError):
            return None

        