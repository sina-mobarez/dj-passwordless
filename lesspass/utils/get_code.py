import pyotp

def get_otp_code(user):
    time_otp = pyotp.TOTP(user.key, interval=180)
    time_otp = time_otp.now()
    return time_otp