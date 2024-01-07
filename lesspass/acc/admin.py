from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


# Register the User model with the custom admin class
admin.site.register(get_user_model())
