from django.test import TestCase
from django.urls import reverse, resolve
from ..views import CustomLoginView, GetCodeView

class TestUrls(TestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_get_code_url_resolves(self):
        url = reverse('get-code')
        self.assertEqual(resolve(url).func.view_class, GetCodeView)
