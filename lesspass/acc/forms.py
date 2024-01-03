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
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username logins.
    """
    
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "id": "usrnme"}))
    otp_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={"id": "otpField"}))

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s. "
            "Fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get("username")
        otp_code = self.cleaned_data.get("otp_code")

        if username is not None:
            self.user_cache = authenticate(
                self.request, username=username, otp_code=otp_code
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": self.username_field.verbose_name},
        )
