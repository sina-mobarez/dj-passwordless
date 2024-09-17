from django.urls import path
from .views import GetCodeView, LoginView, LogoutView

urlpatterns = [
    # Path for getting OTP code view
    path("get_code/", GetCodeView.as_view(), name="get-code"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
