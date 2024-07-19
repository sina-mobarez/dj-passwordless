from utils.send_otp import send_otp
from celery import shared_task

@shared_task
def send_otp_to_phone_number_task(destination, otp):
    """
    Celery task to send OTP to the specified destination (phone number).

    Args:
        destination (str): The destination for sending the OTP (e.g., phone number).
        otp (str): The OTP code to be sent.

    Returns:
        Any: The result of sending the OTP (you may customize the return type based on your needs).
    """
    print(otp, '#######################################')
    return send_otp(destination, otp)
