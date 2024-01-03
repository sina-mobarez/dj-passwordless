from ippanel import Client, HTTPError, Error, ResponseCode
from django.conf import settings
from core.logger import logger

api_key = settings.ACCESS_KEY

sms = Client(api_key)


def send_otp(destination, otp_code):
    """
    Send an OTP message to the specified destination.

    Args:
        destination (str): The phone number to which the OTP message should be sent.
        otp_code (str): The OTP code to be included in the message.

    Raises:
        Error: If there is an error in sending the OTP message.
        HTTPError: If there is an HTTP-related error, such as a network error.

    Example:
        send_otp("123456789", "123456")
    """

    try:
        sms.send_pattern(
            settings.PATTERN_KEY,
            "+983000505",
            f"98{destination}",
            {"verification-code": otp_code},
        )
    except Error as e:
        logger.error(f"Error handled => code: {e.code}, message: {e.message}")
        if e.code == ResponseCode.ErrUnprocessableEntity.value:
            for field in e.message:
                logger.error(f"Field: {field} , Errors: {e.message[field]}")
    except HTTPError as e:
        logger.error(f"HTTPError handled => code: {e}")
