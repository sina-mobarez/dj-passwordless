from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import path
from acc.views import LandingPageView

# Register the User model with the custom admin class


class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("login/", LandingPageView.as_view(), name="login"),
        ]
        return custom_urls + urls


admin_site = CustomAdminSite(name="custom_admin")
admin.site.register(get_user_model())
