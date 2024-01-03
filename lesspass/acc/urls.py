from django.urls import path
from .views import CustomLoginView, GetCodeView

urlpatterns = [
    # Path for custom login view
    path('login/', CustomLoginView.as_view(), name='login'),

    # Path for getting OTP code view
    path('get_code/', GetCodeView.as_view(), name='get-code'),
]