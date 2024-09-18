from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate


class GetPhoneNumberSerializer(serializers.Serializer):
    """
    Serializer for validating phone numbers.
    """

    phone_number = serializers.CharField(
        max_length=10,
        # validators=[
        #     RegexValidator(
        #         regex=r"^9\d{9}$",
        #         message="Phone number must be in the format 9xxxxxxxxx with up to 10 digits.",
        #     ),
        # ],
    )


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=10,
        # validators=[
        #     RegexValidator(
        #         regex=r"^9\d{9}$",
        #         message="Phone number must be in the format 9xxxxxxxxx with up to 10 digits.",
        #     ),
        # ],
    )
    otp_code = serializers.CharField(max_length=6)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Credentials")
