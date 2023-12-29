from time import sleep

def send_otp(destination, otp_code):
    sleep(5)
    return f'otp_code sent to {destination}, and code is {otp_code}'