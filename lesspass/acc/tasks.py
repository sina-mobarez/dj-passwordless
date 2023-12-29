from utils.send_otp import send_otp
from celery import shared_task

@shared_task
def send_otp_to_phone_number_task(des, otp):
    return send_otp(des, otp)