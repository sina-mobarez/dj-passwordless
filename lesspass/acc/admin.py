from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

class CustomUserAdmin(UserAdmin):
    # Add any custom configurations for your User model admin here
    pass

# Register the User model with the custom admin class
admin.site.register(get_user_model(), CustomUserAdmin)
