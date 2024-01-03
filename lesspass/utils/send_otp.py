from ippanel import Client, HTTPError, Error, ResponseCode
from django.conf import settings


api_key = settings.ACCESS_KEY

sms = Client(api_key)

def send_otp(destination, otp_code):
    try:
        sms.send_pattern(settings.PATTERN_KEY, "+983000505", f"98{destination}", {'verification-code': otp_code})
    except Error as e:
        print(f"Error handled => code: {e.code}, message: {e.message}")
        if e.code == ResponseCode.ErrUnprocessableEntity.value:
            for field in e.message:
                print(f"Field: {field} , Errors: {e.message[field]}")
    except HTTPError as e: # http error like network error, not found, ...
        print(f"Error handled => code: {e}")

