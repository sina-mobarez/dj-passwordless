import unicodedata
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UsernameField(forms.CharField):
    def to_python(self, value):
        value = super().to_python(value)
        if self.max_length is not None and len(value) > self.max_length:
            return value
        return unicodedata.normalize("NFKC", value)

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "username",
        }
        
class CustomAuthenticationForm(forms.Form):
    
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "id": "usrnme"}))
    otp_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={"id": "otpField"}))

   