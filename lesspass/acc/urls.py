from django.urls import path
from .views import CustomLoginView, GetCodeView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('get_code/', GetCodeView.as_view(), name='get-code'),
]
