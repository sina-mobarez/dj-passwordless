import pyotp

def generate_otp_code(user):
    """
    Generate a one-time password (OTP) code for the given user using TOTP.

    Args:
        user: The user for whom the OTP code is generated.

    Returns:
        str: The generated OTP code.
    """
    time_otp = pyotp.TOTP(user.key, interval=180).now()
    return str(time_otp)
