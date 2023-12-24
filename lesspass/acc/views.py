
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm



class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    authentication_form = None
    template_name = "registration/login.html"
    redirect_authenticated_user = False
    extra_context = None
