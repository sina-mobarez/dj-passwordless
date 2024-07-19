from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import login

from .forms import CustomAuthenticationForm
from .serializers import GetPhoneNumberSerializer
from .tasks import send_otp_to_phone_number_task
from utils.get_code import generate_otp_code
from core.logger import logger



class CustomLoginView(FormView):
    """
    Custom login view using the CustomAuthenticationForm.
    """

    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"
    success_url = reverse_lazy('landing-page')

    def form_valid(self, form):
        phone = form.cleaned_data['username']
        code = form.cleaned_data['otp_code']
        user = get_user_model().objects.get(phone_number=phone)
        if user:
            login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid otp code.')
        return super().form_invalid(form)


class GetCodeView(APIView):
    """
    API view for getting OTP code based on the provided phone number.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to generate and send OTP code.

        Args:
            request: The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: HTTP response with the result of OTP code generation and sending.
        """
        # Validate input data
        serializer = GetPhoneNumberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract phone number from validated data
        phone_number = serializer.validated_data['phone_number']

        # Get or create user based on the phone number
        user, created = get_user_model().objects.get_or_create(phone_number=phone_number, is_active=True)

        if created:
            logger.info(f"User created with phone number: {phone_number}")

        # Generate OTP code and send it asynchronously
        otp_code = generate_otp_code(user)
        send_otp_to_phone_number_task.delay(phone_number, otp_code)

        return Response({'message': 'OTP Code sent successfully.'}, status=status.HTTP_200_OK)



class LandingPageView(TemplateView):
    template_name = 'successful-login.html'