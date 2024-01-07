from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

    def test_custom_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'registration/login.html')


class GetCodeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.get_code_url = reverse('get-code')

    def test_get_code_view_post(self):
        # Add a test for POST request to GetCodeView
        phone_number = '9876543210'
        data = {'phone_number': phone_number}
        response = self.client.post(self.get_code_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'OTP Code sent successfully.')


