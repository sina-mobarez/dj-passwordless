from rest_framework import serializers
from django.core.validators import RegexValidator


class GetPhoneNumberSerializer(serializers.Serializer):

    phone_number = serializers.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^9\d{9}$',
                message='Phone number must be in the format 9xxxxxxxxx up to 10 digits.',
            ),
        ],
    )