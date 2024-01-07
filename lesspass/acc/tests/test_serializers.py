from django.test import TestCase
from ..serializers import GetPhoneNumberSerializer

class TestGetPhoneNumberSerializer(TestCase):
    def test_valid_phone_number(self):
        data = {'phone_number': '9123456789'}
        serializer = GetPhoneNumberSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_phone_number_format(self):
        data = {'phone_number': '1234567890'}  # Invalid format
        serializer = GetPhoneNumberSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone_number', serializer.errors)

    def test_invalid_phone_number_length(self):
        data = {'phone_number': '91234567891234567890'}  # Invalid length
        serializer = GetPhoneNumberSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone_number', serializer.errors)
